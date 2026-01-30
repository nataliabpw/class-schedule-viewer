from pathlib import Path
import pandas as pd

def main():
    project_root = Path(__file__).parent.parent
    data_path = project_root / 'data' / 'example_schedule.xls'

    df = pd.read_excel(data_path)
    print(df.head())

if __name__ == "__main__":
    main()