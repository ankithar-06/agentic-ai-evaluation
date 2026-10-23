
import subprocess
import sys


def run_script(script_name):
    print(f"\n{'=' * 45}")
    print(f"Running {script_name}")
    print("=" * 45)

    subprocess.run(
        [sys.executable, script_name],
        check=True
    )


def main():
    try:
        run_script("evaluator.py")
        run_script("report.py")
        run_script("compare_agents.py")
        run_script("comparison_agent.py")

        print("\nAll tasks completed successfully!")
        print("Check the CSV files, charts, and PDF report.")

    except subprocess.CalledProcessError as error:
        print(f"\nProject stopped because {error.cmd} failed.")
        print("Fix the error above and run main.py again.")


if __name__ == "__main__":
    main()
