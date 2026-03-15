import os

from fastapi import FastAPI, HTTPException
from uuid import uuid4

from schemas import (
    CreateQuestionRequest,
    CreateQuestionResponse,
    StudentSubmissionRequest,
    StudentSubmissionResponse,
    ClassificationResult,
    ClassInsightsResponse,
    StudentInsightsResponse,
)
from storage import (
    questions_store,
    submissions_store,
    student_memory_store,
    class_memory_store,
    insight_events_store,
)
from insight_engine import (
    generate_insight_events,
    save_insight_events,
    get_class_insight_events,
    get_student_insight_events,
)
from classifier import classify_submission
from memory_service import update_memories, get_student_memories, get_class_memories
from teacher_insights import summarize_class_memories, summarize_student_memories
from moorcheh_memory import upload_memory_record, search_memory
from embeddings import get_embedding

app = FastAPI(title="Teacher-AIde Backend")

@app.get("/")
def root():
    return {"message": "Teacher-AIde backend is running"}

@app.post("/questions", response_model=CreateQuestionResponse)
def create_question(payload: CreateQuestionRequest):
    question_id = f"q_{uuid4().hex[:8]}"

    question_data={
        "question_id": question_id,
        "teacher_id": payload.teacher_id,
        "classroom_id": payload.classroom_id,
        "concept": payload.concept,
        "prompt": payload.prompt,
        "code_snippet": payload.code_snippet,
        "correct_answer": payload.correct_answer
    }

    questions_store[question_id] = question_data

    return CreateQuestionResponse(question_id=question_id, message="Question created successfully")

@app.get("/questions")
def get_all_questions():
    return {"questions": list(questions_store.values())}

@app.post("/submissions", response_model=ClassificationResult)
def create_submission(payload: StudentSubmissionRequest):
    if payload.question_id not in questions_store:
        raise HTTPException(status_code=404, detail="Question not found")

    submission_id = f"sub_{uuid4().hex[:8]}"

    submission_data = {
        "submission_id": submission_id,
        "student_id": payload.student_id,
        "question_id": payload.question_id,
        "student_answer": payload.student_answer,
        "student_reasoning": payload.student_reasoning
    }

    submissions_store[submission_id] = submission_data

    question_data = questions_store[payload.question_id]
    classification = classify_submission(question_data, submission_data)

    update_memories(
        classroom_id=question_data["classroom_id"],
        student_id=payload.student_id,
        concept=question_data["concept"],
        classification=classification,
    )

    events = generate_insight_events(
        classroom_id=question_data["classroom_id"],
        student_id=payload.student_id,
        concept=question_data["concept"],
        classification=classification,
    )
    save_insight_events(events)

    return ClassificationResult(
        submission_id=submission_id,
        is_correct=classification["is_correct"],
        bug_category=classification["bug_category"],
        reasoning_pattern=classification["reasoning_pattern"],
        misconception=classification["misconception"],
        confidence=classification["confidence"],
        evidence=classification["evidence"],
        message="Submission classified successfully"
    )

@app.get("/submissions")
def get_all_submissions():
    return {"submissions": list(submissions_store.values())}

@app.get("/memory/student/{student_id}")
def read_student_memory(student_id: str):
    return {"student_id": student_id, "memories": get_student_memories(student_id)}


@app.get("/memory/class/{classroom_id}")
def read_class_memory(classroom_id: str):
    return {"classroom_id": classroom_id, "memories": get_class_memories(classroom_id)}

@app.get("/insights/class/{classroom_id}", response_model=ClassInsightsResponse)
def get_class_insights(classroom_id: str):
    memories = get_class_memories(classroom_id)
    return summarize_class_memories(classroom_id, memories)


@app.get("/insights/student/{student_id}", response_model=StudentInsightsResponse)
def get_student_insights(student_id: str):
    memories = get_student_memories(student_id)
    return summarize_student_memories(student_id, memories)

@app.get("/events/class/{classroom_id}")
def read_class_events(classroom_id: str):
    return {
        "classroom_id": classroom_id,
        "events": get_class_insight_events(classroom_id)
    }


@app.get("/events/student/{student_id}")
def read_student_events(student_id: str):
    return {
        "student_id": student_id,
        "events": get_student_insight_events(student_id)
    }


@app.get("/events/debug")
def read_all_events():
    return insight_events_store

@app.post("/moorcheh/test-upload")
def moorcheh_test_upload():
    dummy_record = {
        "classroom_id": "grade10_cs",
        "concept": "loops",
        "misconception": "misunderstands Python range upper bound exclusivity",
        "count": 3,
        "students_affected": ["student_001", "student_002"],
        "trend": "persistent",
    }

    result = upload_memory_record(
        record_id="class-memory-test-1",
        record_type="class_memory",
        record=dummy_record
    )

    return {"status": "uploaded", "result": result}

@app.get("/moorcheh/test-search")
def moorcheh_test_search():
    results = search_memory("loop misconception recurring issue", top_k=5)
    return results

@app.get("/deepseek/debug-env")
def deepseek_debug_env():
    key = os.getenv("DEEPSEEK_API_KEY")
    return {
        "api_key_present": key is not None,
        "api_key_length": len(key) if key else 0,
        "api_key_prefix": key[:7] if key else None
    }

@app.get("/embeddings/debug")
def embeddings_debug():
    text = "loops recurring misconception range upper bound"
    vector = get_embedding(text)
    return {
        "length": len(vector),
        "first_10": vector[:10]
    }