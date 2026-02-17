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
                group_index = cell.index(group)
                if group_index+len(group) < len(cell):
                    if cell[group_index+len(group)] in '0123456789':
                        continue
                classes[row_id-start_row] = df.iloc[class_name_row, column_id].strip()+" - "+cell
    return classes

def format_schedule_with_time(classes, df, start_row, time_column_id):
    last_class = None
    schedule = []
    for row_id, curr_class in enumerate(classes):

        if last_class is not None and curr_class!=last_class:
            end_time = df.iloc[row_id+start_row-1, time_column_id]
            end_time = end_time[end_time.index('-')+1:].strip()
            schedule.append({
                "name": last_class,
                "start": start_time,
                "end": end_time
            })

        if curr_class is not None and curr_class!=last_class:
            start_time = df.iloc[row_id+start_row, time_column_id]
            start_time = start_time[:start_time.index('-')].strip()

        last_class = curr_class
    return schedule