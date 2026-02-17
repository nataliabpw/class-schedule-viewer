from datetime import date
from pathlib import Path
from schedule.reader import load_spreadsheet_with_merged_cells
from schedule.matcher import find_columns_for_specific_weekday, find_columns_with_matching_date, is_next_weekday_reached, is_weekday_start_column_id_set

WEEKDAYS = ['PONIEDZIAŁEK', 'WTOREK', 'ŚRODA', 'CZWARTEK', 'PIĄTEK']

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
    
    print(f"Data: {selected_date}\nDzień tygodnia: {WEEKDAYS[weekday_id]}")

    # Future-improvement:  Detect the weekday_row containing weekdays dynamically
    weekday_row = 2

    weekday_start_column_id, weekday_end_column_id = find_columns_for_specific_weekday(df, weekday_id, weekday_row, WEEKDAYS)
    
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

    print_schedule_with_time(classes, df, start_row, time_column_id)

def get_date_from_user():
    # print("Please enter a date: ")
    # day = input("Day: ")
    # month = input("Month: ")
    # year = input("Year: ")
    # return date(int(year), int(month), int(day))
    return date(2025, 11, 7) # Hardcoded for testing

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

def build_group_schedule(class_name_row, start_row, end_row, matching_date_columns, df, group_seminaria, group_cwiczenia, group_zajecia):
    classes = [None] * (end_row - start_row)

    for column_id in matching_date_columns:
        if 'ćwiczenia' in df.iloc[class_name_row, column_id].lower():
            group = group_cwiczenia
        elif 'zajęcia praktyczne' in df.iloc[class_name_row, column_id].lower():
            group = group_zajecia
        else:
            group = group_seminaria
        for row_id in range(start_row, end_row):
            cell = str(df.iloc[row_id, column_id]).strip()
            if group in cell:
                if cell.index(group)+len(group) < len(cell):
                    if cell[cell.index(group)+len(group)] in '0123456789':
                        continue
                classes[row_id-start_row] = df.iloc[class_name_row, column_id].strip()+" - "+cell
    return classes

def print_schedule_with_time(classes, df, start_row, time_column_id):
    last_class = None
    for row_id, curr_class in enumerate(classes):

        if last_class is not None and curr_class!=last_class:
            end_time = df.iloc[row_id+start_row-1, time_column_id]
            end_time = end_time[end_time.index('-')+1:].strip()
            print(f"Koniec: {end_time}")

        if curr_class is not None and curr_class!=last_class:
            print(f"Zajęcia: {curr_class}")
            start_time = df.iloc[row_id+start_row, time_column_id]
            start_time = start_time[:start_time.index('-')].strip()
            print(f"Początek: {start_time}")
        last_class = curr_class

if __name__ == "__main__":
    main()