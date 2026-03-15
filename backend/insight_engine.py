from datetime import datetime
from storage import insight_events_store
from memory_service import get_class_memories, get_student_memories
from moorcheh_memory import upload_memory_record


def generate_insight_events(classroom_id: str, student_id: str, concept: str, classification: dict):
    events = []
    bug_category = classification["bug_category"]
    misconception = classification["misconception"]

    class_memories = get_class_memories(classroom_id)
    student_memories = get_student_memories(student_id)

    for mem in class_memories:
        if mem["concept"] == concept and mem["bug_category"] == bug_category:
            if mem["count"] == 3:
                events.append({
                    "type": "class_insight",
                    "severity": "medium",
                    "classroom_id": classroom_id,
                    "concept": concept,
                    "bug_category": bug_category,
                    "misconception": misconception,
                    "message": f"{misconception} is now emerging as a class-wide issue.",
                })
            elif mem["count"] == 5:
                events.append({
                    "type": "class_insight",
                    "severity": "high",
                    "classroom_id": classroom_id,
                    "concept": concept,
                    "bug_category": bug_category,
                    "misconception": misconception,
                    "message": f"{misconception} is now a dominant misconception in this class.",
                })

    for mem in student_memories:
        if mem["concept"] == concept and mem["bug_category"] == bug_category:
            if mem["count"] == 2:
                events.append({
                    "type": "student_insight",
                    "severity": "medium",
                    "student_id": student_id,
                    "concept": concept,
                    "bug_category": bug_category,
                    "misconception": misconception,
                    "message": f"{student_id} is showing a recurring misunderstanding in {concept}.",
                })
            elif mem["count"] == 3:
                events.append({
                    "type": "student_insight",
                    "severity": "high",
                    "student_id": student_id,
                    "concept": concept,
                    "bug_category": bug_category,
                    "misconception": misconception,
                    "message": f"{student_id} has repeatedly struggled with the same misconception in {concept}.",
                })

    return events


def save_insight_events(events: list):
    now = datetime.utcnow().isoformat()

    for event in events:
        event_id = f"event_{len(insight_events_store) + 1}"

        insight_events_store[event_id] = {
            "event_id": event_id,
            "timestamp": now,
            **event
        }

        upload_memory_record(
            record_id=event_id,
            record_type="insight_event",
            record=insight_events_store[event_id]
        )


def get_class_insight_events(classroom_id: str):
    return [event for event in insight_events_store.values() if event.get("classroom_id") == classroom_id]


def get_student_insight_events(student_id: str):
    return [event for event in insight_events_store.values() if event.get("student_id") == student_id]
