from datetime import date
from pathlib import Path
import pandas as pd

WEEKDAYS = ['PONIEDZIAŁEK','WTOREK','ŚRODA','CZWARTEK','PIĄTEK']

def main():
    project_root = Path(__file__).parent.parent
    data_path = project_root / 'data' / 'example_schedule.xls'

    df = pd.read_excel(data_path)

    SCHEDULE_NAME = df.columns[0]
    print(f"Schedule Name: {SCHEDULE_NAME}")

    date = get_date_from_user()
    weekday_id = date.weekday()  # Monday is 0 and Sunday is 6
    if weekday_id > 4:
        print("No classes on weekends!")
        return
    print(f"Date: {date}\nDay of the week: {WEEKDAYS[weekday_id]}")

    # TO-DO:  Detect the row containing weekdays dynamically
    # NOTE: Currently using hardcoded row index (1), which works only for the specific format
    weekday_row = 1
    weekday_start_column_id = -1
    weekday_end_column_id = df.iloc[weekday_row].size

    for column_id, cell in enumerate(df.iloc[weekday_row]):
        if str(cell).strip() == WEEKDAYS[weekday_id]:
            weekday_start_column_id = column_id
        elif is_weekday_start_column_id_set(weekday_start_column_id) and pd.notna(cell):
            weekday_end_column_id = column_id - 3
            break
    
    print(f"Columns: {weekday_start_column_id} - {weekday_end_column_id}")

def get_date_from_user():
    # print("Please enter a date: ")
    # day = input("Day: ")
    # month = input("Month: ")
    # year = input("Year: ")
    # return date(int(year), int(month), int(day))
    return date(2025, 11, 7) # Hardcoded for testing

def is_weekday_start_column_id_set(weekday_start_column_id):
    if weekday_start_column_id==-1:
        return False
    else:
        return True

if __name__ == "__main__":
    main()