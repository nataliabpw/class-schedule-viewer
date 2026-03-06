from pathlib import Path
from readers.schedule_reader import load_spreadsheet_with_merged_cells
from readers.classrooms_reader import build_classroom_schedule

project_root = Path(__file__).parent.parent
data_dir = project_root / 'data'

files = [
    {
        "name_xlsx": "winter_semester_schedule.xlsx", 
        "name_csv": "winter_semester_schedule.csv",
        "classrooms_csv": "winter_semester_classrooms.csv",
        "end_row": 57,
    },
    {
        "name_xlsx": "summer_semester_schedule.xlsx", 
        "name_csv": "summer_semester_schedule.csv",
        "classrooms_csv": "summer_semester_classrooms.csv",
        "end_row": 60
    },
]

for file in files:
    data_path = data_dir / file["name_xlsx"]
    output_path = data_dir / file["name_csv"]
    classrooms_path = data_dir / file["classrooms_csv"]

    df = load_spreadsheet_with_merged_cells(data_path, file["end_row"])
    df.to_csv(output_path, index=False, header=False)

    classroom_schedule = build_classroom_schedule(data_path, file["end_row"])
    classroom_schedule.to_csv(classrooms_path, index=False, header=False)
