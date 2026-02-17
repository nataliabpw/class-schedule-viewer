from datetime import datetime

def find_columns_for_specific_weekday(df, weekday_id, weekday_row, WEEKDAYS):
    weekday_start_column_id = -1
    weekday_end_column_id = df.iloc[weekday_row].size-1

    for column_id, cell in enumerate(df.iloc[weekday_row]):
        if str(cell).strip() == WEEKDAYS[weekday_id] and not is_weekday_start_column_id_set(weekday_start_column_id):
            weekday_start_column_id = column_id
        elif is_weekday_start_column_id_set(weekday_start_column_id) and weekday_id==4:
            return weekday_start_column_id, weekday_end_column_id
        elif is_next_weekday_reached(weekday_start_column_id, cell, weekday_id):
            weekday_end_column_id = column_id - 3
            return weekday_start_column_id, weekday_end_column_id
    return weekday_start_column_id, weekday_end_column_id

def find_columns_with_matching_date(df, selected_date, weekday_start_column_id, weekday_end_column_id, date_row):
    matching_date_columns = []
    for column_id, cell in enumerate(df.iloc[date_row, weekday_start_column_id:weekday_end_column_id+1]):
        current_column_id = column_id+weekday_start_column_id

        if isinstance(cell, datetime):
            if cell.date() == selected_date:
                matching_date_columns.append(current_column_id)
            continue
        cell = str(cell).strip()

        DASH = '-'
        if DASH in cell:
            dash_index = cell.index(DASH)
            start_date = cell[0:dash_index].strip()
            end_date = cell[dash_index+1:].strip()

            start_date = parse_date(start_date, selected_date)
            end_date = parse_date(end_date, selected_date)

            # handle January case
            if start_date>end_date:
                end_date = end_date.replace(year=end_date.year + 1)

            if start_date <= selected_date <= end_date:
                if is_date_an_exception(cell, selected_date):
                    print(cell)
                    continue
                matching_date_columns.append(current_column_id)
        elif cell=='cały semestr':
            matching_date_columns.append(current_column_id )
        elif cell != 'nan':
            date_from_cell = parse_date(cell, selected_date)
            if date_from_cell==selected_date:
                matching_date_columns.append(current_column_id )
    return matching_date_columns

def is_next_weekday_reached(weekday_start_column_id, cell, weekday_id):
    if is_weekday_start_column_id_set(weekday_start_column_id) and str(cell).strip() == WEEKDAYS[weekday_id+1]:
        return True
    return False

def is_weekday_start_column_id_set(weekday_start_column_id):
    if weekday_start_column_id==-1:
        return False
    return True

def is_date_an_exception(cell, selected_date):
    cell = cell.lower()
    if 'bez' not in cell:
        return False
    BEZ_LENGTH = 3
    bez_end_id = cell.index('bez') + BEZ_LENGTH
    exceptions = cell[bez_end_id:]
    date_to_check = selected_date.strftime("%d.%m")
    if date_to_check in exceptions:
        return True
    return False

def parse_date(date_string, reference_date):
    if date_string[-1]==')':
        id = date_string.index('(')
        date_string = date_string[:id].strip()
    if date_string[-1]!='.':
        date_string += '.'
    if len(date_string)<10:
        if is_reference_date_from_next_year(date_string, reference_date):
            date_string += str(reference_date.year-1)
        else:
            date_string += str(reference_date.year)
    return datetime.strptime(date_string, "%d.%m.%Y").date()

def is_reference_date_from_next_year(date_to_format, reference_date):
    if int(date_to_format[-3:-1]) - reference_date.month > 7:
        return True
    return False