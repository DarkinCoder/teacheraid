from pydantic import BaseModel
from typing import Optional, List

class CreateQuestionRequest(BaseModel):
    teacher_id: str
    classroom_id: str
    concept: str
    prompt: str
    code_snippet: Optional[str] = None
    correct_answer: str

class CreateQuestionResponse(BaseModel):
    question_id: str
    message: str

class StudentSubmissionRequest(BaseModel):
    student_id: str
    question_id: str
    student_answer: str
    student_reasoning: str

class StudentSubmissionResponse(BaseModel):
    submission_id: str
    message: str

class ClassificationResult(BaseModel):
    submission_id: str
    is_correct: bool
    bug_category: str
    reasoning_pattern: str
    misconception: str
    confidence: float
    evidence: List[str]
    message: str

class MisconceptionSummary(BaseModel):
    concept: str
    misconception: str
    count: int
    trend: str

class ClassInsightsResponse(BaseModel):
    classroom_id: str
    top_misconceptions: List[MisconceptionSummary]
    suggested_reteach_topics: List[str]
    teacher_summary: str

class StudentInsightsResponse(BaseModel):
    student_id: str
    recurring_misconceptions: List[MisconceptionSummary]
    suggested_interventions: List[str]
    teacher_summary: str