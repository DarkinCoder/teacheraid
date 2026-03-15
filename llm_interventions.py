from deepseek_client import get_deepseek_client


def generate_class_reteach_topics(classroom_id: str, top_misconceptions: list) -> list[str]:
    try:
        client = get_deepseek_client()

        system_prompt = (
            "You are an educational assistant helping a Grade 10 programming teacher. "
            "Generate 2 to 3 concise reteach actions based on class-wide misconceptions. "
            "Return JSON only."
        )

        user_prompt = f"""
Classroom ID: {classroom_id}

Top misconceptions:
{top_misconceptions}

Return JSON with exactly this format:
{{
  "suggested_reteach_topics": [
    "string",
    "string",
    "string"
  ]
}}

Requirements:
- Focus on immediate classroom reteaching actions
- Keep each suggestion concise and practical
- Tailor the suggestions to Grade 10 programming
"""

        response = client.chat.completions.create(
            model="deepseek-chat",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=250,
        )

        import json
        parsed = json.loads(response.choices[0].message.content)
        return parsed.get("suggested_reteach_topics", [])

    except Exception as e:
        return [f"Reteach suggestions unavailable: {type(e).__name__}"]


def generate_student_interventions(student_id: str, recurring_misconceptions: list) -> list[str]:
    try:
        client = get_deepseek_client()

        system_prompt = (
            "You are an educational assistant helping a Grade 10 programming teacher. "
            "Generate 2 to 3 concise support interventions for one student based on recurring misconceptions. "
            "Return JSON only."
        )

        user_prompt = f"""
Student ID: {student_id}

Recurring misconceptions:
{recurring_misconceptions}

Return JSON with exactly this format:
{{
  "suggested_interventions": [
    "string",
    "string",
    "string"
  ]
}}

Requirements:
- Focus on practical teacher actions
- Keep each suggestion concise and supportive
- Tailor the suggestions to Grade 10 programming
"""

        response = client.chat.completions.create(
            model="deepseek-chat",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=250,
        )

        import json
        parsed = json.loads(response.choices[0].message.content)
        return parsed.get("suggested_interventions", [])

    except Exception as e:
        return [f"Interventions unavailable: {type(e).__name__}"]
