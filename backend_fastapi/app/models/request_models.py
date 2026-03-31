from pydantic import BaseModel
from typing import Optional, Dict, List

class ProcessResponse(BaseModel):
    success: bool
    question: Optional[str] = None
    options: Optional[Dict[str, str]] = None
    answers: List[str] = []
    confidence: Optional[float] = None
    message: Optional[str] = None