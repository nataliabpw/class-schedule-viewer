from datetime import date
from pathlib import Path
from src.schedule.reader import load_spreadsheet_with_merged_cells
from src.schedule.matcher import find_columns_for_specific_weekday, find_columns_with_matching_date, is_next_weekday_reached, is_weekday_start_column_id_set
from src.schedule.builder import build_group_schedule, format_schedule_with_time
from src.schedule.constants import WEEKDAYS

def main():
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'

    df = load_spreadsheet_with_merged_cells(data_dir)

    schedule_name = df.iloc[0,0]
    print(f"Nazwa planu: {schedule_name}")

    selected_date = get_date_from_user()
    weekday_id = selected_date.weekday()  # Monday is 0 and Sunday is 6

    group_seminaria, group_cwiczenia, group_zajecia = get_group_names_from_user()
    
    if weekday_id > 4:
        print("Brak zajęć w weekend!")
        return
    
    print(f"Data: {selected_date}")
    print(f"Dzień tygodnia: {WEEKDAYS[weekday_id]}")

    # Future-improvement:  Detect the weekday_row containing weekdays dynamically
    weekday_row = 2

    weekday_start_column_id, weekday_end_column_id = find_columns_for_specific_weekday(df, weekday_id, weekday_row)
    
    date_row = weekday_row + 2
    matching_date_columns = find_columns_with_matching_date(df, selected_date, weekday_start_column_id, weekday_end_column_id, date_row)

    class_name_row = weekday_row + 1
    start_row = weekday_row + 4
    end_row = df.shape[0]

    classes = build_group_schedule(class_name_row, start_row, end_row, matching_date_columns, df, group_seminaria, group_cwiczenia, group_zajecia)
    
    # Future-improvement: detect time_column_id dynamically
    if weekday_id==0:
        time_column_id = weekday_start_column_id - 2
    else:
        time_column_id = weekday_start_column_id - 1 

    schedule = format_schedule_with_time(classes, df, start_row, time_column_id)
    for entry in schedule:
        print(entry)

def get_date_from_user():
    # print("Please enter a date: ")
    # day = input("Day: ")
    # month = input("Month: ")
    # year = input("Year: ")
    # return date(int(year), int(month), int(day))
    return date(2025, 11, 4) # Hardcoded for testing

def get_group_names_from_user():
    # print("Wprowadź grupy zajęć lub pozostaw puste, jeśli chcesz użyć domyślnych wartości:")
    # group_seminaria = input("Grupa na seminaria: ")
    # group_cwiczenia = input("Grupa na ćwiczenia: ")
    # grupa_zajecia = input("Grupa na zajęcia praktyczne: ")
    # if group_seminaria == "":
    #     group_seminaria = "1"
    # if group_cwiczenia == "":
    #     group_cwiczenia = "1a"
    # if group_zajecia == "":
    #     group_zajecia = "1a"
    
    # group_seminaria = 'grupa ' + group_seminaria.strip()
    # group_cwiczenia = ' ' + group_cwiczenia.strip()
    # group_zajecia = ' ' + group_zajecia.strip()

    # return group_seminaria, group_cwiczenia, group_zajecia
    return 'grupa 1', ' 1a', ' 1a' # Hardcoded for testing

if __name__ == "__main__":
    main()