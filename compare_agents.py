
import csv
import time
from agent import run_agent
from evaluator import load_questions, calculate_metrics, estimate_tokens


def run_version_a(question):
    """Current demo agent."""
    return run_agent(question)


def run_version_b(question):
    """Second demo version with a different response."""
    return {
        "answer": (
            "Artificial intelligence and machine learning "
            "help computers perform tasks using data."
        ),
        "response_time": 0.0,
        "input_tokens": 0,
        "output_tokens": 0,
    }


def evaluate_version(agent_function, question, expected):
    start = time.perf_counter()
    result = agent_function(question)
    elapsed = time.perf_counter() - start

    metrics = calculate_metrics(result["answer"], expected)

    return {
        "answer": result["answer"],
        "response_time_seconds": round(elapsed, 6),
        "input_tokens_estimated": estimate_tokens(question),
        "output_tokens_estimated": estimate_tokens(result["answer"]),
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "f1_score": metrics["f1_score"],
    }


def main():
    questions = load_questions()
    results = []

    agents = {
        "Agent A": run_version_a,
        "Agent B": run_version_b,
    }

    for item in questions:
        for agent_name, agent_function in agents.items():
            metrics = evaluate_version(
                agent_function,
                item["question"],
                item["expected_answer"],
            )

            results.append({
                "question_id": item["id"],
                "agent": agent_name,
                "question": item["question"],
                **metrics,
                "total_tokens_estimated": (
                    metrics["input_tokens_estimated"]
                    + metrics["output_tokens_estimated"]
                ),
            })

    with open(
        "agent_comparison.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys(),
        )
        writer.writeheader()
        writer.writerows(results)

    print("\n--- Agent Comparison ---")

    for agent_name in agents:
        agent_results = [
            row for row in results if row["agent"] == agent_name
        ]

        avg_time = sum(
            row["response_time_seconds"] for row in agent_results
        ) / len(agent_results)

        avg_f1 = sum(
            row["f1_score"] for row in agent_results
        ) / len(agent_results)

        total_tokens = sum(
            row["total_tokens_estimated"] for row in agent_results
        )

        print(f"\n{agent_name}")
        print(f"Average response time: {avg_time:.6f} seconds")
        print(f"Average F1 score: {avg_f1:.4f}")
        print(f"Estimated tokens: {total_tokens}")

    print("\nSaved detailed comparison to agent_comparison.csv")


if __name__ == "__main__":
    main()
