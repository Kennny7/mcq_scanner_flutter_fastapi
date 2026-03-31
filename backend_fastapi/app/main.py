from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import process_image
from app.core.logger import app_logger

app = FastAPI(title="MCQ Scanner API")

# CORS for Flutter frontend (allow all for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(process_image.router, prefix="/api", tags=["process"])

@app.get("/")
async def root():
    return {"message": "MCQ Scanner API is running"}

@app.on_event("startup")
async def startup_event():
    app_logger.info("Starting up MCQ Scanner API...")

@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("Shutting down MCQ Scanner API...")