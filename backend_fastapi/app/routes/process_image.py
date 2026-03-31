from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.text_processor import TextProcessor
from app.services.question_solver import QuestionSolver
from app.models.request_models import ProcessResponse
from app.core.logger import app_logger
from app.core.config import settings

router = APIRouter()

text_processor = TextProcessor()
question_solver = QuestionSolver()

@router.post("/process-image", response_model=ProcessResponse)
async def process_image(file: UploadFile = File(...)):
    """
    Accept an image, run OCR to extract MCQ, search for answers, and return results.
    """
    try:
        # Read image bytes
        image_bytes = await file.read()

        # Step 1: OCR
        extracted_text, confidence = text_processor.extract_text(image_bytes)
        app_logger.info(f"OCR confidence: {confidence}")

        if confidence < settings.OCR_CONFIDENCE_THRESHOLD:
            return ProcessResponse(
                success=False,
                message=f"Low OCR confidence ({confidence:.2f})"
            )

        # Step 2: Parse MCQ
        question, options = text_processor.parse_mcq(extracted_text)

        if not text_processor.is_valid_question(question, options):
            return ProcessResponse(
                success=False,
                message="No valid MCQ format detected"
            )

        # Step 3: Search for answers
        answers = question_solver.search_question(question, options)

        return ProcessResponse(
            success=True,
            question=question,
            options=options,
            answers=answers,
            confidence=confidence,
            message="Processing complete"
        )

    except Exception as e:
        app_logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))