from datetime import datetime
from storage import student_memory_store, class_memory_store
from moorcheh_memory import upload_memory_record


def update_student_memory(student_id: str, concept: str, classification: dict):
    bug_category = classification["bug_category"]
    misconception = classification["misconception"]

    key = f"{student_id}:{concept}:{bug_category}"
    now = datetime.utcnow().isoformat()

    if key not in student_memory_store:
        student_memory_store[key] = {
            "student_id": student_id,
            "concept": concept,
            "bug_category": bug_category,
            "misconception": misconception,
            "count": 1,
            "first_seen": now,
            "last_seen": now,
            "trend": "new",
            "confidence_history": [classification["confidence"]],
            "reasoning_patterns": [classification["reasoning_pattern"]],
            "evidence_examples": [classification.get("evidence", [])],
        }
    else:
        student_memory_store[key]["count"] += 1
        student_memory_store[key]["last_seen"] = now
        student_memory_store[key]["trend"] = "recurring"
        student_memory_store[key]["confidence_history"].append(classification["confidence"])
        student_memory_store[key]["reasoning_patterns"].append(classification["reasoning_pattern"])
        student_memory_store[key]["evidence_examples"].append(classification.get("evidence", []))

    upload_memory_record(
        record_id=f"student-{student_id}-{concept}-{bug_category}",
        record_type="student_memory",
        record=student_memory_store[key]
    )


def update_class_memory(classroom_id: str, student_id: str, concept: str, classification: dict):
    bug_category = classification["bug_category"]
    misconception = classification["misconception"]

    key = f"{classroom_id}:{concept}:{bug_category}"
    now = datetime.utcnow().isoformat()

    if key not in class_memory_store:
        class_memory_store[key] = {
            "classroom_id": classroom_id,
            "concept": concept,
            "bug_category": bug_category,
            "misconception": misconception,
            "count": 1,
            "students_affected": [student_id],
            "first_seen": now,
            "last_seen": now,
            "trend": "emerging",
        }
    else:
        class_memory_store[key]["count"] += 1
        class_memory_store[key]["last_seen"] = now

        if student_id not in class_memory_store[key]["students_affected"]:
            class_memory_store[key]["students_affected"].append(student_id)

        if class_memory_store[key]["count"] >= 3:
            class_memory_store[key]["trend"] = "persistent"
        else:
            class_memory_store[key]["trend"] = "emerging"

    upload_memory_record(
        record_id=f"class-{classroom_id}-{concept}-{bug_category}",
        record_type="class_memory",
        record=class_memory_store[key]
    )


def update_memories(classroom_id: str, student_id: str, concept: str, classification: dict):
    update_student_memory(student_id, concept, classification)
    update_class_memory(classroom_id, student_id, concept, classification)


def get_student_memories(student_id: str):
    return [value for value in student_memory_store.values() if value["student_id"] == student_id]


def get_class_memories(classroom_id: str):
    return [value for value in class_memory_store.values() if value["classroom_id"] == classroom_id]