from llm_teacher_feedback import (
    generate_class_teacher_summary,
    generate_student_teacher_summary,
)
from llm_interventions import (
    generate_class_reteach_topics,
    generate_student_interventions,
)

def summarize_class_memories(classroom_id: str, memories: list) -> dict:
    sorted_memories = sorted(memories, key=lambda x: x["count"], reverse=True)

    top_misconceptions = []
    for mem in sorted_memories[:3]:
        top_misconceptions.append({
            "concept": mem["concept"],
            "misconception": mem["misconception"],
            "count": mem["count"],
            "trend": mem["trend"],
        })

    suggested_reteach_topics = generate_class_reteach_topics(
        classroom_id=classroom_id,
        top_misconceptions=top_misconceptions,
    )

    teacher_summary = generate_class_teacher_summary(
        classroom_id=classroom_id,
        top_misconceptions=top_misconceptions,
        suggested_reteach_topics=suggested_reteach_topics,
    )

    return {
        "classroom_id": classroom_id,
        "top_misconceptions": top_misconceptions,
        "suggested_reteach_topics": suggested_reteach_topics,
        "teacher_summary": teacher_summary,
    }


def summarize_student_memories(student_id: str, memories: list) -> dict:
    sorted_memories = sorted(memories, key=lambda x: x["count"], reverse=True)

    recurring_misconceptions = []
    for mem in sorted_memories[:3]:
        recurring_misconceptions.append({
            "concept": mem["concept"],
            "misconception": mem["misconception"],
            "count": mem["count"],
            "trend": mem["trend"],
        })

    suggested_interventions = generate_student_interventions(
        student_id=student_id,
        recurring_misconceptions=recurring_misconceptions,
    )
    
    teacher_summary = generate_student_teacher_summary(
        student_id=student_id,
        recurring_misconceptions=recurring_misconceptions,
        suggested_interventions=suggested_interventions,
    )

    return {
        "student_id": student_id,
        "recurring_misconceptions": recurring_misconceptions,
        "suggested_interventions": suggested_interventions,
        "teacher_summary": teacher_summary,
    }


def generate_reteach_topic(concept: str, misconception: str) -> str:
    misconception_lower = misconception.lower()

    if "range upper bound" in misconception_lower or "upper bound exclusivity" in misconception_lower:
        return "Reteach how Python range() excludes the upper bound using loop tracing examples."

    if "assignment" in misconception_lower and "comparison" in misconception_lower:
        return "Reteach the difference between assignment (=) and comparison (==) in conditionals."

    if "variable tracing" in misconception_lower:
        return "Reteach variable updates step-by-step with tracing tables."

    return f"Review the concept '{concept}' with targeted examples addressing: {misconception}."


def generate_student_intervention(concept: str, misconception: str) -> str:
    misconception_lower = misconception.lower()

    if "range upper bound" in misconception_lower or "upper bound exclusivity" in misconception_lower:
        return "Give this student a short tracing exercise on Python range() boundaries."

    if "assignment" in misconception_lower and "comparison" in misconception_lower:
        return "Give this student a debugging activity focused on = versus ==."

    if "variable tracing" in misconception_lower:
        return "Give this student a step-by-step variable tracing worksheet."

    return f"Provide targeted support for {concept}: {misconception}."