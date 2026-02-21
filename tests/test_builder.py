from schedule.builder import build_group_schedule, format_schedule_with_time
import pandas as pd

def test_build_group_schedule_cwiczenia():
    df = pd.DataFrame([
        ["Anatomia ćwiczenia", "Biochemia - ćwiczenia"],
        ["grupa 2a 2b", "grupa 12b"],
        ["grupa 2a", "grupa 2b"],
        ["", ""],
        ["grupa 2b", "grupa 14a s. 202b"],
        ["", ""]
    ])

    classes = build_group_schedule(
        class_name_row=0,
        start_row=1,
        end_row=df.shape[0],
        matching_date_columns=[0, 1],
        df=df,
        group_seminaria="grupa 1",
        group_cwiczenia=" 2b",
        group_zajecia=" 2a"
    )

    assert classes == [
        "Anatomia ćwiczenia - grupa 2a 2b",
        "Biochemia - ćwiczenia - grupa 2b",
        None,
        "Anatomia ćwiczenia - grupa 2b",
        None
    ]

def test_build_group_schedule_for_group_1():
    df = pd.DataFrame([
        ["Prawo medyczne", "Biochemia seminarium"],
        ["grupa 1", "grupa 13"],
        ["grupa 11", "grupa 1 s. 101"],
        ["", "grupa 11"],
        ["grupa 1", "grupa 15 s. 201b"],
        ["", ""]
    ])

    classes = build_group_schedule(
        class_name_row=0,
        start_row=1,
        end_row=df.shape[0],
        matching_date_columns=[0, 1],
        df=df,
        group_seminaria="grupa 1",
        group_cwiczenia=" 1a",
        group_zajecia=" 1b"
    )

    assert classes == [
        "Prawo medyczne - grupa 1",
        "Biochemia seminarium - grupa 1 s. 101",
        None,
        "Prawo medyczne - grupa 1",
        None
    ]

def test_format_schedule_with_time():
    classes = [
        "Prawo medyczne - grupa 1",
        "Prawo medyczne - grupa 1",
        "Prawo medyczne - grupa 1",
        "Anatomia ćwiczenia - grupa 1a",
        None,
        "Biochemia - grupa 1",
        "Biochemia - grupa 1",
        None
    ]

    df = pd.DataFrame([
        ["08.00 - 09.00"],
        ["09.00 - 10.00"],
        ["10.00 - 11.00"],
        ["11.00 - 12.00"],
        ["12.00 - 13.00"],
        ["13.00 - 14.00"],
        ["14.00 - 15.00"],
        [""]
    ])

    schedule = format_schedule_with_time(
        classes=classes,
        df=df,
        start_row=0,
        time_column_id=0
    )

    expected_schedule = [
        {"name": "Prawo medyczne - grupa 1", "start": "08.00", "end": "11.00"},
        {"name": "Anatomia ćwiczenia - grupa 1a", "start": "11.00", "end": "12.00"},
        {"name": "Biochemia - grupa 1", "start": "13.00", "end": "15.00"},
    ]

    assert schedule == expected_schedule