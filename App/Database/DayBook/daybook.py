import os
import json
from datetime import datetime

class DayBookSystem:
    @staticmethod
    def get_path():
        path = os.path.join(os.path.dirname(__file__), "daybook.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    @staticmethod
    def load_records():
        try:
            with open(DayBookSystem.get_path(), "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_records(records):
        with open(DayBookSystem.get_path(), "w") as f:
            json.dump(records, f, indent=4)

    @staticmethod
    def add_record(record):
        records = DayBookSystem.load_records()
        records.append(record)
        DayBookSystem.save_records(records)

    @staticmethod
    def show_day_book():
        records = DayBookSystem.load_records()

        print("" + "=" * 95)
        print("DAY BOOK".center(95))
        print("=" * 95)
        print(f"{'DATE':<20}{'USERNAME':<15}{'FULL NAME':<22}{'AMOUNT':<12}{'TYPE':<12}{'STATUS'}")
        print("-" * 95)

        if not records:
            print("No day book records found.")
            print("=" * 95)
            return

        for rec in records[-20:]:
            print(
                f"{rec.get('date', ''):<20}"
                f"{rec.get('username', ''):<15}"
                f"{rec.get('fullname', ''):<22}"
                f"Rs.{rec.get('amount', 0):<10}"
                f"{rec.get('type', ''):<12}"
                f"{rec.get('status', '')}"
            )

        print("=" * 95)