"""Script to generate sample process event log data as CSV."""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


ACTIVITIES = [
    "Register Request",
    "Examine Casually",
    "Examine Thoroughly",
    "Check Ticket",
    "Decide",
    "Reject Request",
    "Pay Compensation",
    "Reinitiate Request",
]

RESOURCES = ["Alice", "Bob", "Carol", "Dave", "Ellen"]


def generate_log(num_cases: int = 20, seed: int = 42) -> list[dict]:
    random.seed(seed)
    rows = []
    base = datetime(2024, 3, 1, 8, 0, 0)

    for i in range(1, num_cases + 1):
        case_id = f"case-{i:04d}"
        num_events = random.randint(3, len(ACTIVITIES))
        activities = random.sample(ACTIVITIES, num_events)
        timestamp = base + timedelta(days=random.randint(0, 30))

        for activity in activities:
            rows.append(
                {
                    "case_id": case_id,
                    "activity": activity,
                    "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
                    "resource": random.choice(RESOURCES),
                }
            )
            timestamp += timedelta(minutes=random.randint(10, 240))

    return rows


def save_csv(rows: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["case_id", "activity", "timestamp", "resource"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} events to {output_path}")


if __name__ == "__main__":
    rows = generate_log(num_cases=20)
    save_csv(rows, Path(__file__).parent / "sample_log.csv")
