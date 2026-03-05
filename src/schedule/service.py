import pandas as pd
from pathlib import Path
from datetime import date
from .reader import load_spreadsheet_with_merged_cells
from .matcher import find_columns_for_specific_weekday, find_columns_with_matching_date, is_next_weekday_reached, is_weekday_start_column_id_set
from .builder import build_group_schedule, format_schedule_with_time, build_classroom_schedule
from .constants import WEEKDAYS

def get_schedule_for_date_and_groups(selected_date, group_seminaria, group_cwiczenia, group_zajecia):
    weekday_id = selected_date.weekday()  # Monday is 0 and Sunday is 6
    
    if weekday_id > 4:
        return {
            "schedule_name": "",
            "selected_date": selected_date.strftime("%Y-%m-%d"),
            "weekday": WEEKDAYS[weekday_id],
            "schedule": []
        }
    
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'data'
    
    weekday_row = 2
    class_name_row = weekday_row + 1
    start_row = weekday_row + 4

    summer_semester_start = date(2026, 2, 16)
    if selected_date >= summer_semester_start:
        file_name ='summer_semester_schedule.csv'
        classroom_file_name = 'summer_semester_schedule.xlsx'
        date_row = weekday_row + 3
        class_info_row = weekday_row + 2
        end_row = 60
    else:
        file_name ='winter_semester_schedule.csv'
        classroom_file_name = 'winter_semester_schedule.xlsx'
        date_row = weekday_row + 2
        class_info_row = weekday_row + 3
        end_row = 57

    data_path = data_dir / file_name
    classroom_data_path = data_dir / classroom_file_name
    df = pd.read_csv(data_path, header=None)
    
    schedule_name = df.iloc[0,0]

    weekday_start_column_id, weekday_end_column_id = find_columns_for_specific_weekday(df, weekday_id, weekday_row)
    
    matching_date_columns = find_columns_with_matching_date(df, selected_date, weekday_start_column_id, weekday_end_column_id, date_row)

    classes = build_group_schedule(class_name_row, class_info_row, start_row, end_row, matching_date_columns, df, group_seminaria, group_cwiczenia, group_zajecia)
    
    # Future-improvement: detect time_column_id dynamically
    if weekday_id==0:
        time_column_id = weekday_start_column_id - 2
    else:
        time_column_id = weekday_start_column_id - 1 

    schedule = format_schedule_with_time(classes, df, start_row, time_column_id)

    classroom_schedule = build_classroom_schedule(classroom_data_path, end_row)

    return {
    "schedule_name": schedule_name,
    "selected_date": selected_date.strftime("%Y-%m-%d"),
    "weekday": WEEKDAYS[weekday_id],
    "schedule": schedule,
    "classroom_schedule": classroom_schedule
    }