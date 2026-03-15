MISCONCEPTION_TAXONOMY = {
    "loops": {
        "misunderstanding_range_bounds": "Misunderstands that Python range() excludes the stop value",
        "off_by_one_loop": "Makes off-by-one loop errors",
        "infinite_loop_risk": "Does not understand how loop termination works",
        "loop_variable_update_confusion": "Misunderstands how loop variables change across iterations",
    },
    "conditionals": {
        "assignment_vs_comparison": "Confuses assignment with comparison in conditionals",
        "condition_logic_error": "Misunderstands how conditional logic is evaluated",
        "else_branch_misread": "Misinterprets when the else branch executes",
    },
    "variables": {
        "variable_tracing_error": "Has difficulty tracing variable values through code",
        "value_overwrite_confusion": "Misunderstands how reassignment overwrites values",
        "string_number_confusion": "Confuses strings and numbers in program behavior",
    },
    "lists": {
        "index_starts_at_one": "Assumes list indexing starts at 1 instead of 0",
        "out_of_bounds_confusion": "Misunderstands valid list index ranges",
        "append_vs_assign_confusion": "Confuses appending an item with assigning to an index",
    }
}

FALLBACK_LABEL = "unclear_or_other"


def get_allowed_labels(concept: str) -> list[str]:
    concept = concept.lower()
    labels = list(MISCONCEPTION_TAXONOMY.get(concept, {}).keys())
    labels.append(FALLBACK_LABEL)
    return labels


def get_canonical_display_label(concept: str, bug_category: str) -> str:
    concept = concept.lower()
    return MISCONCEPTION_TAXONOMY.get(concept, {}).get(
        bug_category,
        "Unclear or other misconception"
    )