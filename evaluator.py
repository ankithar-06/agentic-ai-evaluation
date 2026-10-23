
import json
import csv
import re
from collections import Counter
from agent import run_agent


def load_questions():
    with open("questions.json", "r", encoding="utf-8") as file:
        return json.load(file)


def tokenize(text):
    """Convert text to lowercase word tokens."""
    return re.findall(r"\b\w+\b", text.lower())


def calculate_metrics(actual, expected):
    """
    Calculate word-level precision, recall, and F1.
    These are baseline text similarity metrics, not semantic accuracy.
    """
    actual_tokens = tokenize(actual)
    expected_tokens = tokenize(expected)

    if not actual_tokens or not expected_tokens:
        return {
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0
        }

    actual_counts = Counter(actual_tokens)
    expected_counts = Counter(expected_tokens)
    common = sum((actual_counts & expected_counts).values())

    precision = common / len(actual_tokens)
    recall = common / len(expected_tokens)

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0.0
    )

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4)
    }


def estimate_tokens(text):
    """
    Rough local estimate only.
    This is not the model's actual tokenizer count.
    """
    return len(tokenize(text))


def run_evaluation():
    questions = load_questions()
    results = []

    for item in questions:
        print(f"Evaluating question {item['id']}...")

        result = run_agent(item["question"])
        metrics = calculate_metrics(
            result["answer"],
            item["expected_answer"]
        )

        input_tokens = estimate_tokens(item["question"])
        output_tokens = estimate_tokens(result["answer"])

        results.append({
            "question_id": item["id"],
            "question": item["question"],
            "expected_answer": item["expected_answer"],
            "actual_answer": result["answer"],
            "response_time_seconds": result["response_time"],
            "input_tokens_estimated": input_tokens,
            "output_tokens_estimated": output_tokens,
            "total_tokens_estimated": input_tokens + output_tokens,
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1_score": metrics["f1_score"]
        })

    if not results:
        print("No questions found. Add questions to questions.json.")
        return

    with open(
        "performance_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    average_time = sum(
        row["response_time_seconds"] for row in results
    ) / len(results)

    average_f1 = sum(
        row["f1_score"] for row in results
    ) / len(results)

    total_tokens = sum(
        row["total_tokens_estimated"] for row in results
    )

    print("\n--- Evaluation Summary ---")
    print(f"Questions evaluated: {len(results)}")
    print(f"Average response time: {average_time:.4f} seconds")
    print(f"Average F1 score: {average_f1:.4f}")
    print(f"Estimated total tokens: {total_tokens}")
    print("Saved results to performance_results.csv")


if __name__ == "__main__":
    run_evaluation()
