import os

DATASET_PATH = "ai_model/dataset/r4.2-1"


def load_employee_logs():

    employee_logs = {}

    if not os.path.exists(DATASET_PATH):
        print("Dataset folder not found!")
        return employee_logs

    files = [f for f in os.listdir(DATASET_PATH) if f.endswith(".csv")]

    print(f"\nFound {len(files)} employee log files.\n")

    for file in files:

        filepath = os.path.join(DATASET_PATH, file)

        try:

            events = []

            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:

                for line in f:

                    line = line.strip()

                    if line:
                        events.append(line)

            employee_logs[file] = events

            print(f"Loaded {file} ({len(events)} events)")

        except Exception as e:

            print(f"Failed: {file} -> {e}")

    return employee_logs


if __name__ == "__main__":

    logs = load_employee_logs()

    print("\n===================================")
    print("Employees Loaded :", len(logs))
    print("===================================")