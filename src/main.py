from datetime import datetime, date
from pathlib import Path
import pandas as pd
import numpy as np

WEEKDAYS = ['PONIEDZIAŁEK', 'WTOREK', 'ŚRODA', 'CZWARTEK', 'PIĄTEK']

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
        elif is_next_weekday_reached(weekday_start_column_id, cell):
            weekday_end_column_id = column_id - 3
            break
    
    print(f"Columns: {weekday_start_column_id} - {weekday_end_column_id}")
    
    date_row = weekday_row + 2
    matching_date_columns = []
    for column_id, cell in enumerate(df.iloc[date_row, weekday_start_column_id:weekday_end_column_id+1]):
        current_column_id = column_id+weekday_start_column_id

        # Obsługa kolumny typu numpy.float64
        if isinstance(cell, (float, np.floating)):
            col_name = df.columns[current_column_id]
            df[col_name] = df[col_name].astype("object")

        if isinstance(cell, datetime):
            if cell.date() == date:
                matching_date_columns.append(current_column_id)
            continue
        cell = str(cell).strip()
        # cell = "".join(cell.split())
        if cell=='nan':
            df.iloc[date_row, current_column_id] = df.iloc[date_row, current_column_id-1]
            cell = str(df.iloc[date_row, current_column_id-1]).strip()
        DASH = '-'
        if DASH in cell:
            dash_index = cell.index(DASH)
            start_date = cell[0:dash_index].strip()
            end_date = cell[dash_index+1:].strip()

            # zamiana str na datę
            start_date = format_date(start_date, date)
            end_date = format_date(end_date, date)
            # obsługa stycznia
            if start_date>end_date:
                end_date = end_date.replace(year=end_date.year + 1)

            # (sprawdzenie czy zakres pasuje do daty)
            if start_date <= date <= end_date:
                # (jeśli tak to zapamiętanie kolumny)
                matching_date_columns.append(current_column_id)
        elif cell=='cały semestr':
            matching_date_columns.append(current_column_id )
        elif cell != 'nan':
            date_from_cell = format_date(cell, date)
            if date_from_cell==date:
                matching_date_columns.append(current_column_id )
    print(matching_date_columns)

def get_date_from_user():
    # print("Please enter a date: ")
    # day = input("Day: ")
    # month = input("Month: ")
    # year = input("Year: ")
    # return date(int(year), int(month), int(day))
    return date(2025, 11, 6) # Hardcoded for testing

def is_next_weekday_reached(weekday_start_column_id, cell):
    if is_weekday_start_column_id_set(weekday_start_column_id) and pd.notna(cell):
        return True
    return False

def is_weekday_start_column_id_set(weekday_start_column_id):
    if weekday_start_column_id==-1:
        return False
    else:
        return True

def format_date(date_to_format, date_for_year):
    # TO-DO
    # dodać obsługę komentarza (bez xx.yy)
    # teraz komentarz jest pomijany
    if date_to_format[-1]==')':
        id = date_to_format.index('(')
        date_to_format = date_to_format[:id].strip()
    if date_to_format[-1]!='.':
        date_to_format += '.'
    if len(date_to_format)<10:
        date_to_format += str(date_for_year.year)
    return datetime.strptime(date_to_format, "%d.%m.%Y").date()

if __name__ == "__main__":
    main()