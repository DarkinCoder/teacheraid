from deepseek_client import get_deepseek_client

def generate_class_teacher_summary(classroom_id: str, top_misconceptions: list, suggested_reteach_topics: list) -> str:
    try:
        client = get_deepseek_client()

        system_prompt = (
            "You are an educational assistant helping a Grade 10 programming teacher. "
            "Write a short, clear, teacher-friendly summary based on class misconception data. "
            "Keep it concise, actionable, and professional."
        )

        user_prompt = f"""
Classroom ID: {classroom_id}

Top misconceptions:
{top_misconceptions}

Suggested reteach topics:
{suggested_reteach_topics}

Write 2-4 sentences explaining:
1. what the class seems to be struggling with
2. why it matters
3. what the teacher should do next
"""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=200,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Teacher summary unavailable: {type(e).__name__}"


def generate_student_teacher_summary(student_id: str, recurring_misconceptions: list, suggested_interventions: list) -> str:
    try:
        client = get_deepseek_client()

        system_prompt = (
            "You are an educational assistant helping a Grade 10 programming teacher. "
            "Write a short, clear, teacher-friendly summary about one student's recurring programming misconceptions. "
            "Keep it concise, actionable, and supportive."
        )

        user_prompt = f"""
Student ID: {student_id}

Recurring misconceptions:
{recurring_misconceptions}

Suggested interventions:
{suggested_interventions}

Write 2-4 sentences explaining:
1. what this student is repeatedly struggling with
2. what kind of support might help next
"""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=200,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Teacher summary unavailable: {type(e).__name__}"
