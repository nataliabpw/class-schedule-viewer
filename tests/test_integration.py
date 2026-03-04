import pandas as pd
from datetime import date
from schedule.matcher import find_columns_for_specific_weekday, find_columns_with_matching_date
from schedule.builder import build_group_schedule, format_schedule_with_time

def test_full_flow_with_mock_df():
    weekday_row = ["", "PONIEDZIAŁEK", "PONIEDZIAŁEK", "PONIEDZIAŁEK", "", "", "WTOREK"]
    class_name_row = ["", "Anatomia ćwiczenia",  "Anatomia ćwiczenia", "Biochemia zajęcia praktyczne", "", "", "Prawo medyczne"]
    dates_row = ["", "08.12.", "03.11. - 24.11.", "03.11. - 15.12 (bez 10.11, 08.12)", "", "", "cały semestr"]
    class_info_row = ["", "sala 1", "sala 2", "sala 3", "", "", "sala 4"]

    df = pd.DataFrame([
        weekday_row,
        class_name_row,
        dates_row,
        class_info_row,
        ["08.00 - 09.00", "grupa 1a", "grupa 4b", "grupa 1b", "", "", "grupa 3"],
        ["09.00 - 10.00", "grupa 2b", "grupa 1a", "grupa 1a", "", "", "grupa 3"],
        ["10.00 - 11.00", "grupa 3a", "grupa 1a", "grupa 4b", "", "", "grupa 1"],
        ["","", "", "", "", "", ""]
    ])

    selected_date = date(2025, 11, 17)
    weekday_id = selected_date.weekday()

    start, end = find_columns_for_specific_weekday(df, weekday_id, weekday_row=0)

    matching_date_columns = find_columns_with_matching_date(df, selected_date, start, end, date_row=2)
    start_row = 4

    classes = build_group_schedule(
        class_name_row=1,
        class_info_row=3,
        start_row=start_row,
        end_row=df.shape[0],
        matching_date_columns=matching_date_columns,
        df=df,
        group_seminaria="grupa 1",
        group_cwiczenia=" 1a",
        group_zajecia=" 1b"
    )

    schedule = format_schedule_with_time(classes, df, start_row=start_row, time_column_id=0)

    assert schedule == [
        {"name": "Biochemia zajęcia praktyczne - grupa 1b", "info": "sala 3", "start": "08.00", "end": "09.00"},
        {"name": "Anatomia ćwiczenia - grupa 1a", "info": "sala 2", "start": "09.00", "end": "11.00"},
    ]