import pandas as pd
from .utils.profiler import timer

@timer
def build_group_schedule(class_name_row, class_info_row, start_row, end_row, matching_date_columns, df, group_seminaria, group_cwiczenia, group_zajecia):
    classes = [None] * (end_row - start_row)

    group_seminaria = str(group_seminaria).strip()
    group_cwiczenia = str(group_cwiczenia).strip()
    group_zajecia = str(group_zajecia).strip()

    for column_id in matching_date_columns:
        if 'ćwiczenia' in df.iloc[class_name_row, column_id].lower():
            group = ' ' + group_cwiczenia
            group_short = group_cwiczenia
        elif 'zajęcia praktyczne' in df.iloc[class_name_row, column_id].lower():
            group = ' ' + group_zajecia
            group_short = group_zajecia
        else:
            group = 'grupa ' + group_seminaria
            group_short = group_seminaria
        
        for row_id in range(start_row, end_row):
            cell = str(df.iloc[row_id, column_id]).strip()

            match = False

            if cell == 'nan':
                continue

            if cell == group_short:
                match = True
            elif group in cell:
                if not group_short[-1].isalpha():
                    # Seminarium
                    group_index = cell.index(group)
                    if group_index+len(group) < len(cell):
                        if cell[group_index+len(group)] in '0123456789':
                            continue
                match = True
            elif group_short[-1].isalpha():
                # Ćwiczenia or Zajęcia praktyczne
                
                pattern = group_seminaria + "abc"
                cell_without_commas_and_spaces = cell.replace(",", "").replace(" ", "")

                if pattern in cell_without_commas_and_spaces:
                    match = True
                else:
                    group_with_spaces = " " + group_short[:-1] + " " + group_short[-1]
                    if group_with_spaces in cell:
                        match = True

            if match:
                name = df.iloc[class_name_row, column_id].strip()+" - "+cell
                location = df.iloc[class_info_row, column_id]
                location = '' if pd.isna(location) else str(location).strip()
                classes[row_id-start_row] = {
                    "name": name, 
                    "location": location
                }
    return classes

@timer
def format_schedule_with_time(classes, df, start_row, time_column_id):
    last_class = None
    schedule = []
    for row_id, curr_class_entry in enumerate(classes):

        curr_class = curr_class_entry["name"] if curr_class_entry is not None else None

        if last_class is not None and curr_class!=last_class:
            end_time = df.iloc[row_id+start_row-1, time_column_id]
            end_time = end_time[end_time.index('-')+1:].strip()
            schedule.append({
                "name": last_class,
                "info": last_class_info,
                "start": start_time,
                "end": end_time
            })

        if curr_class is not None and curr_class!=last_class:
            start_time = df.iloc[row_id+start_row, time_column_id]
            start_time = start_time[:start_time.index('-')].strip()

        last_class = curr_class
        last_class_info = curr_class_entry["location"] if curr_class_entry is not None else None
    return schedule

@timer
def build_classroom_schedule(data_path, end_row):
    df = pd.read_excel(data_path, header=None, skiprows=end_row+1, usecols=[0])
    df = df.dropna()                            
    class_schedule = df.iloc[:-1,0].tolist()
    class_schedule[0] = class_schedule[0].replace("Zajęcia", "\nZajęcia")
    return class_schedule