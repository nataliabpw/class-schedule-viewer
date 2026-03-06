import pandas as pd

def build_classroom_schedule(data_path, end_row):
    df = pd.read_excel(data_path, header=None, skiprows=end_row+1, usecols=[0])
    df = df.dropna()                            
    classroom_schedule = df.iloc[:-1,0]
    classroom_schedule[0] = classroom_schedule[0].replace("Zajęcia", "\nZajęcia")
    return classroom_schedule