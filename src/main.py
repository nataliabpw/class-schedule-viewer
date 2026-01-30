from datetime import date
from pathlib import Path
import pandas as pd

def main():
    project_root = Path(__file__).parent.parent
    data_path = project_root / 'data' / 'example_schedule.xls'

    df = pd.read_excel(data_path)

    SCHEDULE_NAME = df.iloc[0,0]
    print(f"Schedule Name: {SCHEDULE_NAME}")

    date = get_date_from_user()
    print(f"Date: {date}")

def get_date_from_user():
    # print("Please enter a date: ")
    # day = input("Day: ")
    # month = input("Month: ")
    # year = input("Year: ")
    # return date(int(year), int(month), int(day))
    return date(2025, 11, 3) # Hardcoded for testing


if __name__ == "__main__":
    main()