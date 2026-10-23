
import time


def run_agent(question):
    """
    Runs a simple demo agent.
    We will connect this function to a real AI model next.
    """
    start_time = time.perf_counter()

    # Temporary demo response
    answer = f"Demo response for: {question}"

    end_time = time.perf_counter()
    response_time = end_time - start_time

    return {
        "answer": answer,
        "response_time": round(response_time, 4),
        "input_tokens": 0,
        "output_tokens": 0,
    }


if __name__ == "__main__":
    result = run_agent("What is artificial intelligence?")
    print(result)

