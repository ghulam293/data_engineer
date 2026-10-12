
import subprocess
import sys
import csv
import time
from pathlib import Path
from datetime import datetime

# Step 1: Project paths
project_folder = Path(__file__).resolve().parent.parent

scripts_folder = project_folder / "scripts"
reports_folder = project_folder / "reports"
logs_folder = project_folder / "logs"

reports_folder.mkdir(parents=True, exist_ok=True)
logs_folder.mkdir(parents=True, exist_ok=True)

summary_file = reports_folder / "pipeline_summary.csv"
log_file = logs_folder / "pipeline.log"

# Step 2: Scripts to execute
scripts = [
    "validate_sales.py",
    "clean_sales.py",
    "data_quality_report.py",
    "daily_sales.py",
    "analyze_daily_sales.py",
    "create_dashboard.py"
]

# Step 3: Empty summary list
summary = []
# Start the pipeline timer
pipeline_start = time.perf_counter()

# Step 4: Execute scripts one by one
for script in scripts:

    print(f"\nRunning: {script}")

    start_time = datetime.now()
    start_seconds = time.perf_counter()

    try:
        subprocess.run(
            [sys.executable, str(scripts_folder / script)],
            check=True
        )

        status = "SUCCESS"
        print(f"{script}: SUCCESS")
    except subprocess.CalledProcessError:
        status = "FAILED"
        print(f"{script}: FAILED")

    # Calculate execution time
    end_seconds = time.perf_counter()
    duration = round(end_seconds - start_seconds, 2)

    # Record result
    summary.append({
        "script": script,
        "status": status,
        "execution_time": str(start_time),
        "duration_seconds": duration
    })
    # Save log entry
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(
            f"{start_time} | {script} | {status}\n"
        )

    # Stop if a script fails
    if status == "FAILED":
        print("Pipeline stopped due to failure.")
        break

# Step 5: Save summary as CSV
with open(summary_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
    "script",
    "status",
    "execution_time",
    "duration_seconds"
    ]
    )

    writer.writeheader()
    writer.writerows(summary)

print("\nPipeline summary saved to:")
print(summary_file)

# Step 39: Generate performance reports
# Only run if all main scripts succeeded

if summary and all(item["status"] == "SUCCESS" for item in summary):

    performance_scripts = [
        "pipeline_performance.py",
        "pipeline_performance_chart.py"
    ]

    try:
        for script in performance_scripts:
            print("\nGenerating report:", script)

            subprocess.run(
                [sys.executable, str(scripts_folder / script)],
                check=True
            )

        print("\nPerformance reports generated successfully!")

    except subprocess.CalledProcessError:
        print("\nPerformance report generation FAILED")
        sys.exit(1)



# Step 6: Show final status
# Step 6: Calculate total pipeline execution time
pipeline_end = time.perf_counter()

total_duration = round(pipeline_end - pipeline_start, 2)

print("\nTotal pipeline execution time:", total_duration, "seconds")


# Step 7: Find the slowest script
if summary:
    slowest_script = max(
        summary,
        key=lambda item: item["duration_seconds"]
    )

    print("\nSlowest script:", slowest_script["script"])

    print(
        "Execution time:",
        slowest_script["duration_seconds"],
        "seconds"
    )

# Step 47: Record failed pipeline runs

if any(item["status"] == "FAILED" for item in summary):

    print("\nPIPELINE FAILED")

    # Save failure information to health history
    history_file = reports_folder / "pipeline_health_history.csv"

    failed_scripts = sum(
        item["status"] == "FAILED"
        for item in summary
    )

    history_record = {
        "run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pipeline_health": "FAILED",
        "total_scripts": len(summary),
        "successful_scripts": len(summary) - failed_scripts,
        "failed_scripts": failed_scripts,
        "slow_scripts": sum(
            item["duration_seconds"] > 5
            for item in summary
        ),
        "total_duration_seconds": total_duration
    }

    file_exists = history_file.exists()

    with open(history_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(history_record.keys())
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(history_record)

    print("Failed run saved to health history.")
    sys.exit(1)

else:
    print("\nPIPELINE COMPLETED SUCCESSFULLY")
    sys.exit(0)
