
import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("agent_comparison.csv")

    summary = df.groupby("agent").agg(
        average_response_time=("response_time_seconds", "mean"),
        average_f1=("f1_score", "mean"),
        estimated_tokens=("total_tokens_estimated", "sum"),
    )

    print("\n--- Comparison Summary ---")
    print(summary.round(4))

    # Average response time
    summary["average_response_time"].plot(
        kind="bar",
        title="Average Response Time by Agent",
        ylabel="Seconds",
        xlabel="Agent",
    )
    plt.tight_layout()
    plt.savefig("agent_response_comparison.png")
    plt.close()

    # Average F1 score
    summary["average_f1"].plot(
        kind="bar",
        title="Average Word-Level F1 Score by Agent",
        ylabel="F1 score",
        xlabel="Agent",
    )
    plt.tight_layout()
    plt.savefig("agent_f1_comparison.png")
    plt.close()

    # Estimated token consumption
    summary["estimated_tokens"].plot(
        kind="bar",
        title="Estimated Token Consumption by Agent",
        ylabel="Estimated tokens",
        xlabel="Agent",
    )
    plt.tight_layout()
    plt.savefig("agent_token_comparison.png")
    plt.close()

    summary.to_csv("agent_comparison_summary.csv")
    print("\nComparison charts and summary generated.")


if __name__ == "__main__":
    main()
