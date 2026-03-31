from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re
from app.core.logger import app_logger
from app.core.config import settings

class QuestionSolver:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36'
        })

    def search_question(self, question: str, options: dict) -> list:
        """Search question online and find answers. Fallback to Gemini if search fails."""
        search_query = f'"{question}"'

        try:
            search_results = list(search(
                search_query,
                num_results=settings.MAX_SEARCH_RESULTS,
                timeout=settings.SEARCH_TIMEOUT
            ))
            answers = self.analyze_results(search_results, question, options)

            # If no confident answers found, try Gemini
            if not answers or answers == ["Not found"]:
                app_logger.info("No confident answers from web search, falling back to Gemini")
                gemini_answers = self.ask_gemini(question, options)
                return gemini_answers if gemini_answers else ["Not found"]

            return answers

        except Exception as e:
            app_logger.error(f"Search error: {str(e)}")
            # Fallback to Gemini on error
            app_logger.info("Falling back to Gemini due to search error")
            gemini_answers = self.ask_gemini(question, options)
            if gemini_answers:
                return gemini_answers
            else:
                return [f"Error: {str(e)}"]

    def ask_gemini(self, question: str, options: dict) -> list:
        """Use Gemini API to answer the MCQ. Returns list of answer letters."""
        app_logger.info("Entering ask_gemini()")
        if not settings.GEMINI_API_KEY:
            app_logger.warning("Gemini API key not set, skipping fallback")
            return []

        # Construct prompt
        options_text = "\n".join([f"{letter}: {text}" for letter, text in options.items()])
        prompt = f"""You are an expert in AWS certifications. Answer the following multiple choice question. 
    Provide only the letter(s) of the correct answer(s). If multiple are correct, list them separated by commas (e.g., "A, C").

    Question: {question}

    Options:
    {options_text}

    Answer:"""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        try:
            app_logger.info(f"Sending request to Gemini model: {settings.GEMINI_MODEL}")
            response = requests.post(url, json=payload, timeout=30)
            app_logger.info(f"Gemini response status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            app_logger.debug(f"Gemini response data: {data}")

            candidates = data.get("candidates", [])
            if not candidates:
                app_logger.warning("No candidates in Gemini response")
                return []

            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if not parts:
                app_logger.warning("No parts in Gemini response")
                return []

            answer_text = parts[0].get("text", "").strip()
            app_logger.info(f"Gemini answer text: {answer_text}")

            # Normalize to uppercase for case‑insensitive matching
            answer_upper = answer_text.upper()

            # Extract letters A-D using word boundaries
            found_letters = re.findall(r'\b([A-D])\b', answer_upper)
            if not found_letters:
                # Fallback: look for any option letter in the uppercase text
                for letter in options.keys():
                    if letter in answer_upper:
                        found_letters.append(letter)

            unique_letters = list(dict.fromkeys(found_letters))
            if unique_letters:
                app_logger.info(f"Extracted letters: {unique_letters}")
                return unique_letters
            else:
                app_logger.warning(f"Gemini returned no recognizable answer: {answer_text}")
                return []

        except Exception as e:
            app_logger.error(f"Gemini API error: {str(e)}")
            return []


    def analyze_results(self, urls: list, question: str, options: dict) -> list:
        answer_counts = {option: 0 for option in options.keys()}
        total_matches = 0

        for url in urls:
            try:
                page_content = self.extract_page_content(url)
                page_answers = self.find_answers_in_content(page_content, question, options)

                for answer in page_answers:
                    if answer in answer_counts:
                        answer_counts[answer] += 1
                        total_matches += 1
            except Exception as e:
                app_logger.warning(f"Failed to analyze {url}: {str(e)}")
                continue

        if total_matches > 0:
            confident_answers = [
                option for option, count in answer_counts.items()
                if count > 0 and count / total_matches >= 0.3
            ]
            return confident_answers if confident_answers else ["Not found"]

        return ["Not found"]

    def extract_page_content(self, url: str) -> str:
        response = self.session.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        return soup.get_text()

    def find_answers_in_content(self, content: str, question: str, options: dict) -> list:
        found_answers = []
        content_lower = content.lower()
        question_keywords = ' '.join(question.lower().split()[:10])

        for option, option_text in options.items():
            option_lower = option_text.lower()

            if question_keywords in content_lower and option_lower in content_lower:
                found_answers.append(option)

            answer_patterns = [
                f'answer[:\s]+{option}',
                f'correct[:\s]+{option}',
                f'{option}[\.\s]+.*?correct',
            ]
            for pattern in answer_patterns:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    found_answers.append(option)

        return found_answers