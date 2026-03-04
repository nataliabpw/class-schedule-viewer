from pathlib import Path
from .reader import load_spreadsheet_with_merged_cells
from .matcher import find_columns_for_specific_weekday, find_columns_with_matching_date, is_next_weekday_reached, is_weekday_start_column_id_set
from .builder import build_group_schedule, format_schedule_with_time, build_classroom_schedule
from .constants import WEEKDAYS

def get_schedule_for_date_and_groups(selected_date, group_seminaria, group_cwiczenia, group_zajecia):
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'data'
    data_path = data_dir / 'winter_semester_schedule.xlsx'

    df = load_spreadsheet_with_merged_cells(data_path)

    schedule_name = df.iloc[0,0]

    group_seminaria = 'grupa ' + str(group_seminaria)
    group_cwiczenia = ' ' + group_cwiczenia
    group_zajecia = ' ' + group_zajecia

    weekday_id = selected_date.weekday()  # Monday is 0 and Sunday is 6
    
    if weekday_id > 4:
        return {
            "schedule_name": schedule_name,
            "selected_date": selected_date.strftime("%Y-%m-%d"),
            "weekday": WEEKDAYS[weekday_id],
            "schedule": []
        }

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

    classroom_schedule = build_classroom_schedule(data_path)

    return {
    "schedule_name": schedule_name,
    "selected_date": selected_date.strftime("%Y-%m-%d"),
    "weekday": WEEKDAYS[weekday_id],
    "schedule": schedule,
    "classroom_schedule": classroom_schedule
    }