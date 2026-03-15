import json
from deepseek_client import get_deepseek_client
from taxonomy import get_allowed_labels, get_canonical_display_label, FALLBACK_LABEL


def classify_submission(question: dict, submission: dict) -> dict:
    try:
        concept = question.get("concept", "").lower()
        prompt = question.get("prompt", "")
        code_snippet = question.get("code_snippet", "")
        correct_answer = question.get("correct_answer", "")

        student_answer = submission.get("student_answer", "")
        student_reasoning = submission.get("student_reasoning", "")

        allowed_labels = get_allowed_labels(concept)
        client = get_deepseek_client()

        system_prompt = (
            "You are an expert educational AI for Grade 10 programming. "
            "Classify the student's response into exactly one allowed misconception category. "
            "Return valid JSON only."
        )

        user_prompt = f"""
Concept: {concept}

Question:
{prompt}

Code Snippet:
{code_snippet}

Correct Answer:
{correct_answer}

Allowed bug_category labels:
{allowed_labels}

Student Answer:
{student_answer}

Student Reasoning:
{student_reasoning}

Return JSON with exactly these keys:
- is_correct (boolean)
- bug_category (string; must be one of the allowed labels only)
- reasoning_pattern (string)
- misconception (string; short teacher-friendly wording)
- confidence (number from 0 to 1)
- evidence (array of short strings)

Rules:
- bug_category MUST be chosen from the allowed labels exactly
- do not invent a new bug_category
- misconception should be short and teacher-friendly
- confidence must be between 0 and 1
- evidence should quote or paraphrase the student's reasoning briefly
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

        content = response.choices[0].message.content
        parsed = json.loads(content)

        bug_category = parsed.get("bug_category", FALLBACK_LABEL)
        if bug_category not in allowed_labels:
            bug_category = FALLBACK_LABEL

        canonical_label = get_canonical_display_label(concept, bug_category)

        return {
            "is_correct": bool(parsed.get("is_correct", False)),
            "bug_category": bug_category,
            "reasoning_pattern": parsed.get(
                "reasoning_pattern",
                "unable to confidently identify reasoning pattern"
            ),
            "misconception": canonical_label,
            "raw_misconception_text": parsed.get("misconception", canonical_label),
            "confidence": float(parsed.get("confidence", 0.5)),
            "evidence": parsed.get("evidence", []),
        }

    except Exception as e:
        concept = question.get("concept", "").lower()
        return {
            "is_correct": False,
            "bug_category": FALLBACK_LABEL,
            "reasoning_pattern": "fallback classification triggered",
            "misconception": get_canonical_display_label(concept, FALLBACK_LABEL),
            "raw_misconception_text": f"LLM unavailable: {type(e).__name__}",
            "confidence": 0.3,
            "evidence": [str(e)],
        }