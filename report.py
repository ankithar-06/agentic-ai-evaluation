
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def generate_report():
    df = pd.read_csv("performance_results.csv")

    total_questions = len(df)
    avg_time = df["response_time_seconds"].mean()
    avg_f1 = df["f1_score"].mean() * 100
    total_tokens = df["total_tokens_estimated"].sum()

    print("\n--- AI Agent Performance Dashboard ---")
    print(f"Questions evaluated: {total_questions}")
    print(f"Average response time: {avg_time:.4f} seconds")
    print(f"Average F1 score: {avg_f1:.2f}%")
    print(f"Estimated total tokens: {total_tokens}")

    with PdfPages("performance_report.pdf") as pdf:

        # Page 1: Response time chart
        plt.figure(figsize=(9, 5))
        plt.bar(
            df["question_id"].astype(str),
            df["response_time_seconds"]
        )
        plt.title("AI Agent Response Time")
        plt.xlabel("Question ID")
        plt.ylabel("Seconds")
        plt.tight_layout()
        pdf.savefig()
        plt.savefig("response_time.png")
        plt.close()

        # Page 2: F1 score chart
        plt.figure(figsize=(9, 5))
        plt.bar(
            df["question_id"].astype(str),
            df["f1_score"] * 100
        )
        plt.title("AI Agent Word-Level F1 Score")
        plt.xlabel("Question ID")
        plt.ylabel("F1 score (%)")
        plt.ylim(0, 100)
        plt.tight_layout()
        pdf.savefig()
        plt.savefig("f1_score.png")
        plt.close()

        # Page 3: Estimated token consumption
        plt.figure(figsize=(9, 5))
        plt.bar(
            df["question_id"].astype(str),
            df["total_tokens_estimated"]
        )
        plt.title("Estimated Token Consumption")
        plt.xlabel("Question ID")
        plt.ylabel("Estimated tokens")
        plt.tight_layout()
        pdf.savefig()
        plt.savefig("token_consumption.png")
        plt.close()

        # Page 4: Summary
        plt.figure(figsize=(9, 5))
        plt.axis("off")

        summary = (
            "AI AGENT PERFORMANCE REPORT\n\n"
            f"Questions evaluated: {total_questions}\n"
            f"Average response time: {avg_time:.4f} seconds\n"
            f"Average word-level F1 score: {avg_f1:.2f}%\n"
            f"Estimated total tokens: {total_tokens}\n\n"
            "Important notes:\n"
            "- This project currently uses a demo agent.\n"
            "- Token consumption is estimated using word counts.\n"
            "- F1 measures word overlap, not factual correctness."
        )

        plt.text(
            0.08, 0.9, summary,
            fontsize=13,
            verticalalignment="top"
        )
        pdf.savefig()
        plt.close()

    print("\nReport generated successfully!")
    print("Created: performance_report.pdf")
    print("Created: response_time.png")
    print("Created: f1_score.png")
    print("Created: token_consumption.png")


if __name__ == "__main__":
    generate_report()
