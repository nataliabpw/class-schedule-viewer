from openpyxl import load_workbook
import pandas as pd

def load_spreadsheet_with_merged_cells(data_dir):
    # Future improvement:
    # - try converting .xls to .xlsx using LibreOffice or other tool
    converted_data_path = data_dir / 'converted_example_schedule.xlsx'
    df = pd.read_excel(converted_data_path, header=None, nrows=55)
    df = df.astype(object)

    wb = load_workbook(converted_data_path)
    ws = wb.active # first sheet from file

    for merged_range in ws.merged_cells.ranges:

        merged_cell_value = ws.cell(row=merged_range.min_row, column=merged_range.min_col).value
        
        row_start = merged_range.min_row - 1
        row_end   = merged_range.max_row
        col_start = merged_range.min_col - 1
        col_end   = merged_range.max_col

        # df out-of-bounds protection
        if row_end <= df.shape[0] and col_end <= df.shape[1]:
            df.iloc[
                row_start:row_end,
                col_start:col_end
            ] = merged_cell_value
    return df