from moorcheh_client import get_moorcheh_client, MOORCHEH_NAMESPACE
from embeddings import get_embedding


def serialize_memory_record(record_type: str, record: dict) -> str:
    if record_type == "student_memory":
        return (
            f"Student {record['student_id']} in concept {record['concept']} "
            f"has misconception {record['misconception']}. "
            f"Trend: {record['trend']}. Count: {record['count']}."
        )

    if record_type == "class_memory":
        return (
            f"Classroom {record['classroom_id']} in concept {record['concept']} "
            f"has misconception {record['misconception']}. "
            f"Trend: {record['trend']}. Count: {record['count']}. "
            f"Students affected: {len(record['students_affected'])}."
        )

    if record_type == "insight_event":
        return (
            f"Insight event for classroom or student. "
            f"Type: {record.get('type', 'unknown')}. "
            f"Message: {record.get('message', '')}"
        )

    return str(record)


def upload_memory_record(record_id: str, record_type: str, record: dict):
    client = get_moorcheh_client()

    text = serialize_memory_record(record_type, record)
    vector = get_embedding(text)

    vectors = [
        {
            "id": record_id,
            "vector": vector,
            "source": record_type,
            "index": 0
        }
    ]

    return client.upload_vectors(
        namespace_name=MOORCHEH_NAMESPACE,
        vectors=vectors
    )


def search_memory(query_text: str, top_k: int = 5):
    client = get_moorcheh_client()
    query_vector = get_embedding(query_text)

    return client.search(
        namespaces=[MOORCHEH_NAMESPACE],
        query=query_vector,
        top_k=top_k
    )
