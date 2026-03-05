from pathlib import Path
from src.schedule.reader import load_spreadsheet_with_merged_cells

project_root = Path(__file__).parent.parent
data_dir = project_root / 'data'

files = [
    {
        "name_xlsx": "winter_semester_schedule.xlsx", 
        "name_csv": "winter_semester_schedule.csv",
        "end_row": 57,
    },
    {
        "name_xlsx": "summer_semester_schedule.xlsx", 
        "name_csv": "summer_semester_schedule.csv",
        "end_row": 60
    },
]

for file in files:
    data_path = data_dir / file["name_xlsx"]
    output_path = data_dir / file["name_csv"]
    df = load_spreadsheet_with_merged_cells(data_path, file["end_row"])
    df.to_csv(output_path, index=False, header=False)

