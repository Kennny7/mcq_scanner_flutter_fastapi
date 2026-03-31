\# 📱 MCQ Scanner: Flutter + FastAPI



\[!\[Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)

\[!\[FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)](https://fastapi.tiangolo.com/)

\[!\[Flutter](https://img.shields.io/badge/Flutter-3.27-blue?logo=flutter)](https://flutter.dev/)

\[!\[Dart](https://img.shields.io/badge/Dart-3.6-blue?logo=dart)](https://dart.dev/)

\[!\[License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



A modern mobile application that scans MCQ questions from an image, extracts text using OCR, and returns possible answers using a FastAPI backend.



\---



\## ✨ Features



\- 📸 \*\*Real-time camera capture\*\* – built with Flutter and `camera` plugin.

\- 🔍 \*\*OCR extraction\*\* – uses OCR.space API to extract text from images.

\- 🤖 \*\*Answer retrieval\*\* – scrapes search results to find matching answers.

\- 🚀 \*\*FastAPI backend\*\* – efficient, scalable, and easily deployable.

\- 📱 \*\*Cross‑platform\*\* – runs on Android (iOS ready with minimal changes).

\- 🎨 \*\*Clean Material Design UI\*\* – responsive and user‑friendly.



\---



\## 🏗️ Architecture



```mermaid

sequenceDiagram

&#x20;   participant User

&#x20;   participant Flutter

&#x20;   participant FastAPI

&#x20;   participant OCR\_API

&#x20;   participant Search\_API



&#x20;   User->>Flutter: Capture image

&#x20;   Flutter->>FastAPI: POST /process-image (image bytes)

&#x20;   FastAPI->>OCR\_API: Extract text

&#x20;   OCR\_API-->>FastAPI: Raw text

&#x20;   FastAPI->>FastAPI: Parse MCQ (question + options)

&#x20;   FastAPI->>Search\_API: Search for answers

&#x20;   Search\_API-->>FastAPI: Search results

&#x20;   FastAPI-->>Flutter: JSON (question, options, answers, confidence)

&#x20;   Flutter->>User: Display results

```



\---



\## 📁 Project Structure



```bash

mcq\_scanner\_flutter\_fastapi/

├── .git

│   ├── HEAD

│   ├── config

│   ├── description

│   ├── hooks

│   │   ├── applypatch-msg.sample

│   │   ├── commit-msg.sample

│   │   ├── fsmonitor-watchman.sample

│   │   ├── post-update.sample

│   │   ├── pre-applypatch.sample

│   │   ├── pre-commit.sample

│   │   ├── pre-merge-commit.sample

│   │   ├── pre-push.sample

│   │   ├── pre-rebase.sample

│   │   ├── pre-receive.sample

│   │   ├── prepare-commit-msg.sample

│   │   ├── push-to-checkout.sample

│   │   ├── sendemail-validate.sample

│   │   └── update.sample

│   ├── index

│   ├── info

│   │   └── exclude

│   ├── objects

│   └── refs

│       ├── heads

│       └── tags

├── .gitignore

├── .idea

│   ├── .gitignore

│   ├── caches

│   │   └── deviceStreaming.xml

│   ├── deviceManager.xml

│   ├── mcq\_scanner\_flutter\_fastapi.iml

│   ├── modules.xml

│   └── workspace.xml

├── README.md

├── backend\_fastapi

│   ├── .env

│   ├── .gitignore

│   ├── Dockerfile

│   ├── app

│   │   ├── \_\_init\_\_.py

│   │   ├── \_\_pycache\_\_

│   │   ├── core

│   │   ├── main.py

│   │   ├── models

│   │   ├── routes

│   │   └── services

│   ├── requirements.txt

│   └── venv

│       ├── Include

│       ├── Lib

│       ├── Scripts

│       └── pyvenv.cfg

└── frontend\_flutter

&#x20;   ├── .dart\_tool

&#x20;   │   ├── dartpad

&#x20;   │   ├── flutter\_build

&#x20;   │   ├── hooks\_runner

&#x20;   │   ├── package\_config.json

&#x20;   │   ├── package\_graph.json

&#x20;   │   └── version

&#x20;   ├── .env

&#x20;   ├── .flutter-plugins-dependencies

&#x20;   ├── .gitignore

&#x20;   ├── .idea

&#x20;   │   ├── libraries

&#x20;   │   ├── modules.xml

&#x20;   │   ├── runConfigurations

&#x20;   │   └── workspace.xml

&#x20;   ├── .metadata

&#x20;   ├── README.md

&#x20;   ├── analysis\_options.yaml

&#x20;   ├── android

&#x20;   │   ├── .gitignore

&#x20;   │   ├── .gradle

&#x20;   │   ├── .kotlin

&#x20;   │   ├── app

&#x20;   │   ├── build.gradle.kts

&#x20;   │   ├── frontend\_flutter\_android.iml

&#x20;   │   ├── gradle

&#x20;   │   ├── gradle.properties

&#x20;   │   ├── gradlew

&#x20;   │   ├── gradlew.bat

&#x20;   │   ├── local.properties

&#x20;   │   └── settings.gradle.kts

&#x20;   ├── assets

&#x20;   │   ├── icon

&#x20;   │   └── splash

&#x20;   ├── build

&#x20;   │   ├── .cxx

&#x20;   │   ├── app

&#x20;   │   ├── b2f7e7edd35b3c8d4f463bb8b035ecd8.cache.dill.track.dill

&#x20;   │   ├── camera\_android\_camerax

&#x20;   │   ├── flutter\_assets

&#x20;   │   ├── flutter\_native\_splash

&#x20;   │   ├── flutter\_plugin\_android\_lifecycle

&#x20;   │   ├── image\_picker\_android

&#x20;   │   ├── native\_assets

&#x20;   │   ├── native\_hooks

&#x20;   │   ├── path\_provider\_android

&#x20;   │   ├── permission\_handler\_android

&#x20;   │   └── reports

&#x20;   ├── frontend\_flutter.iml

&#x20;   ├── ios

&#x20;   │   ├── .gitignore

&#x20;   │   ├── Flutter

&#x20;   │   ├── Runner

&#x20;   │   ├── Runner.xcodeproj

&#x20;   │   ├── Runner.xcworkspace

&#x20;   │   └── RunnerTests

&#x20;   ├── lib

&#x20;   │   ├── main.dart

&#x20;   │   ├── models

&#x20;   │   ├── screens

&#x20;   │   ├── services

&#x20;   │   └── utils

&#x20;   ├── linux

&#x20;   │   ├── .gitignore

&#x20;   │   ├── CMakeLists.txt

&#x20;   │   ├── flutter

&#x20;   │   └── runner

&#x20;   ├── macos

&#x20;   │   ├── .gitignore

&#x20;   │   ├── Flutter

&#x20;   │   ├── Runner

&#x20;   │   ├── Runner.xcodeproj

&#x20;   │   ├── Runner.xcworkspace

&#x20;   │   └── RunnerTests

&#x20;   ├── pubspec.lock

&#x20;   ├── pubspec.yaml

&#x20;   ├── test

&#x20;   │   └── widget\_test.dart

&#x20;   ├── web

&#x20;   │   ├── favicon.png

&#x20;   │   ├── icons

&#x20;   │   ├── index.html

&#x20;   │   ├── manifest.json

&#x20;   │   └── splash

&#x20;   └── windows

&#x20;       ├── .gitignore

&#x20;       ├── CMakeLists.txt

&#x20;       ├── flutter

&#x20;       └── runner



```



\*For a complete tree, see the repository.\*



\---



\## 🛠️ Prerequisites



\- \*\*Flutter SDK\*\* (latest stable) – \[Installation guide](https://flutter.dev/docs/get-started/install)

\- \*\*Android Studio\*\* (for Android emulator / build)

\- \*\*Python 3.10+\*\*

\- \*\*Git\*\*



\---



\## 🐍 Backend Setup (FastAPI)



\### 1. Clone the repository

```bash

git clone https://github.com/Kennny7/mcq\_scanner\_flutter\_fastapi.git

cd mcq\_scanner\_flutter\_fastapi/backend\_fastapi

```



\### 2. Create and activate a virtual environment

```bash

\# Windows

python -m venv venv

venv\\Scripts\\activate



\# macOS / Linux

python3 -m venv venv

source venv/bin/activate

```



\### 3. Install dependencies

```bash

pip install -r requirements.txt

```



\### 4. Set up environment variables

Create a `.env` file in `backend\_fastapi/` (copy from `.env.example` if present):

```env

OCR\_SPACE\_API\_KEY=your\_ocr\_space\_key\_here

OCR\_CONFIDENCE\_THRESHOLD=0.5

MAX\_SEARCH\_RESULTS=3

SEARCH\_TIMEOUT=15

LOG\_LEVEL=INFO

```

> 💡 Get a free OCR.space API key from \[ocr.space/ocrapi](https://ocr.space/ocrapi).



\### 5. Run the server

```bash

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```

You should see:

```

INFO:     Uvicorn running on http://0.0.0.0:8000

```



\### 6. Test the API

Open your browser at \[http://localhost:8000/docs](http://localhost:8000/docs). The interactive Swagger UI will appear, allowing you to test the `/process-image` endpoint.



\---



\## 📱 Frontend Setup (Flutter)



\### 1. Navigate to frontend directory

```bash

cd ../frontend\_flutter

```



\### 2. Get dependencies

```bash

flutter pub get

```



\### 3. Configure backend URL

Create a `.env` file in `frontend\_flutter/` (or edit `lib/services/api\_service.dart` directly for development):

```env

API\_BASE\_URL=http://10.0.2.2:8000   # Android emulator

\# API\_BASE\_URL=http://192.168.x.x:8000   # Physical device (use your local IP)

```

> \*\*Important\*\*:  

> - For Android emulator, use `10.0.2.2` to refer to the host machine.  

> - For a physical device, use your computer's IPv4 address (e.g., `192.168.1.10`).  

> - Make sure port 8000 is open in your firewall.



\### 4. Run the app on an emulator or device

```bash

\# List available devices

flutter devices



\# Run on a specific device

flutter run -d <device\_id>

```

The app will start and ask for camera permissions.



\---



\## 🔧 Building for Android



\### 1. Ensure `android/app/src/main/AndroidManifest.xml` contains camera permission

```xml

<uses-permission android:name="android.permission.CAMERA" />

<uses-feature android:name="android.hardware.camera" android:required="true" />

```



\### 2. Add app icon and splash screen

We use the `flutter\_native\_splash` package. After adding it to `pubspec.yaml`, run:

```bash

flutter pub run flutter\_native\_splash:create

```

This will generate the splash screen images and update the Android manifest.



\### 3. Build APK

```bash

flutter build apk --release

```

The APK will be located at `build/app/outputs/flutter-apk/app-release.apk`.



\### 4. Test on physical device

\- Enable \*\*Developer options\*\* and \*\*USB debugging\*\* on your Android device.

\- Connect via USB and run `flutter run` or transfer the APK and install it.



\---



\## 🔐 Environment Variables (Detailed)



\### Backend `.env`

| Variable | Description |

|----------|-------------|

| `OCR\_SPACE\_API\_KEY` | Your OCR.space API key (required). |

| `OCR\_CONFIDENCE\_THRESHOLD` | Minimum confidence score (0–1) to accept OCR text. |

| `MAX\_SEARCH\_RESULTS` | Number of search results to analyze. |

| `SEARCH\_TIMEOUT` | Timeout for web requests in seconds. |

| `LOG\_LEVEL` | Logging level (`INFO`, `DEBUG`, etc.). |



\### Frontend `.env`

| Variable | Description |

|----------|-------------|

| `API\_BASE\_URL` | Full URL of the FastAPI backend (e.g., `http://10.0.2.2:8000`). |



> The frontend reads this via `flutter\_dotenv`. Make sure to include `.env` in `.gitignore` to avoid exposing secrets.



\---



\## 🔌 API Endpoints



| Method | Endpoint | Description |

|--------|----------|-------------|

| `GET`  | `/` | Root endpoint – returns `{"message": "MCQ Scanner API is running"}` |

| `POST` | `/api/process-image` | Accepts an image file (`multipart/form-data`) and returns extracted MCQ data and answers. |



\*\*Request example (curl):\*\*

```bash

curl -X POST http://localhost:8000/api/process-image \\

&#x20; -F "file=@/path/to/your/image.jpg"

```



\*\*Response example:\*\*

```json

{

&#x20; "success": true,

&#x20; "question": "What is the capital of France?",

&#x20; "options": {

&#x20;   "A": "Berlin",

&#x20;   "B": "Madrid",

&#x20;   "C": "Paris",

&#x20;   "D": "Lisbon"

&#x20; },

&#x20; "answers": \["C"],

&#x20; "confidence": 0.92,

&#x20; "message": "Processing complete"

}

```



\---



\## 🧪 Testing in Android Studio



1\. Open the `frontend\_flutter` folder in Android Studio as a Flutter project.

2\. Use the \*\*Device Manager\*\* to create an Android emulator (API 34+).

3\. Click the \*\*Run\*\* button or press `Shift + F10`.

4\. The app will build and launch on the emulator.



\---



\## 📦 Deployment Considerations



\- \*\*Backend\*\*: You can deploy the FastAPI app to a cloud server (e.g., AWS EC2, DigitalOcean, or Render) using the provided `Dockerfile`.  

\- \*\*Frontend\*\*: After building the APK, you can distribute it via Google Play Store or direct download.



\---



\## 📜 License



This project is licensed under the \*\*MIT License\*\*. See the \[LICENSE](LICENSE) file for details.



\---



\## 🙏 Acknowledgments



\- \[OCR.space](https://ocr.space/) for their free OCR API.

\- \[FastAPI](https://fastapi.tiangolo.com/) for the awesome web framework.

\- \[Flutter](https://flutter.dev/) for enabling cross-platform development.

\- \[Kivy](https://kivy.org/) – the original framework that inspired this rewrite.



\---



\## 🔗 Useful Links



<div align="center">



\[!\[Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge\&logo=python)](https://www.python.org/)

\[!\[FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=for-the-badge\&logo=fastapi)](https://fastapi.tiangolo.com/)

\[!\[Flutter](https://img.shields.io/badge/Flutter-3.27-blue?style=for-the-badge\&logo=flutter)](https://flutter.dev/)

\[!\[Dart](https://img.shields.io/badge/Dart-3.6-blue?style=for-the-badge\&logo=dart)](https://dart.dev/)

\[!\[OCR.space](https://img.shields.io/badge/OCR.space-API-orange?style=for-the-badge)](https://ocr.space/)

\[!\[GitHub](https://img.shields.io/badge/GitHub-Repo-black?style=for-the-badge\&logo=github)](https://github.com/Kennny7/mcq\_scanner\_flutter\_fastapi)



</div>



\---



> Made with ❤️ by \[Kennny7](https://github.com/Kennny7)

