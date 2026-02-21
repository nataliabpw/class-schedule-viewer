import pandas as pd
from datetime import date
from schedule.matcher import find_columns_for_specific_weekday, parse_date, is_date_an_exception, find_columns_with_matching_date

def test_find_columns_for_monday():
    df = pd.DataFrame([
        ["", "PONIEDZIAŁEK", "PONIEDZIAŁEK", "PONIEDZIAŁEK", "", "", "WTOREK"]
    ])
    
    start, end = find_columns_for_specific_weekday(
        df=df,
        weekday_id=0,   # Monday
        weekday_row=0
    )

    assert start == 1
    assert end == 3

def test_find_columns_for_friday():
    df = pd.DataFrame([
        ["CZWARTEK", "", "", "PIĄTEK", "PIĄTEK", "PIĄTEK", "PIĄTEK"]
    ])
    
    start, end = find_columns_for_specific_weekday(
        df=df,
        weekday_id=4,   # Friday
        weekday_row=0
    )

    assert start == 3
    assert end == 6

def test_parse_date_same_years():
    date_string = "07.11."
    reference_date = date(2025, 11, 14)

    result = parse_date(date_string, reference_date)

    assert result == date(2025, 11, 7)

def test_parse_date_from_year_before_reference():
    date_string = "07.12."
    reference_date = date(2026, 1, 6)

    result = parse_date(date_string, reference_date)

    assert result == date(2025, 12, 7)

def test_date_exception_present():
    cell = "7.11 - 19.12 (bez 14.11, 12.12)"
    selected_date = date(2025, 12, 12)

    result = is_date_an_exception(cell, selected_date)
    
    assert result is True

def test_date_exception_not_present():
    cell = "7.11 - 19.12 (bez 14.11, 12.12)"
    selected_date = date(2025, 12, 19)

    result = is_date_an_exception(cell, selected_date)
    
    assert result is False

def test_date_exception_no_exceptions():
    cell = "7.11 - 19.12"
    selected_date = date(2025, 12, 12)

    result = is_date_an_exception(cell, selected_date)
    
    assert result is False

def test_matching_single_date():
    row = ["7.11.", "09.01", "12.12"]
    df = pd.DataFrame([row])

    result = find_columns_with_matching_date(
        df=df,
        selected_date=date(2025, 12, 12),
        weekday_start_column_id=0,
        weekday_end_column_id=len(row)-1,
        date_row=0
    )

    assert result == [2]

def test_matching_date_range():
    row = ["7.11. - 19.12", "07.11 - 21.11", "12.12 - 19.12"]
    df = pd.DataFrame([row])

    result = find_columns_with_matching_date(
        df=df,
        selected_date=date(2025, 12, 12),
        weekday_start_column_id=0,
        weekday_end_column_id=len(row)-1,
        date_row=0
    )

    assert result == [0, 2]

def test_matching_date_whole_semester():
    row = ["09.01", "cały semestr"]
    df = pd.DataFrame([row])

    result = find_columns_with_matching_date(
        df=df,
        selected_date=date(2025, 12, 12),
        weekday_start_column_id=0,
        weekday_end_column_id=len(row)-1,
        date_row=0
    )

    assert result == [1]

def test_matching_date_range_with_exception():
    row = ["7.11 - 19.12 (bez 12.12)"]
    df = pd.DataFrame([row])

    result = find_columns_with_matching_date(
        df=df,
        selected_date=date(2025, 12, 12),
        weekday_start_column_id=0,
        weekday_end_column_id=0,
        date_row=0
    )

    assert result == []

def test_matching_multiple_date_types():
    row = ["7.11.", "7.11 - 19.12", "07.11 - 21.11", "09.01", "12.12", "cały semestr", "7.11 - 19.12 (bez 12.12)"]
    df = pd.DataFrame([row])

    result = find_columns_with_matching_date(
        df=df,
        selected_date=date(2025, 12, 12),
        weekday_start_column_id=0,
        weekday_end_column_id=len(row)-1,
        date_row=0
    )

    assert result == [1, 4, 5] # range, single date, whole semester
