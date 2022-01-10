# standard imports
import pandas as pd

# custom imports
import os
import sys
modules_path  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Modules"))
if modules_path not in sys.path:
    sys.path.insert(1, modules_path)
import SaveDataAsCSV

# reading csv with cumulative data
path = os.path.abspath(os.path.join(os.path.dirname(__file__), "final_data.csv"))
df = pd.read_csv(path)

df1 = df.iloc[::2]
df2 = df.iloc[1::2]
SaveDataAsCSV.df_to_csv_in_dir(dataframe=df1, caller_path=__file__, relative_target_path="../Analytics/Pallav", csv_filename="pallav_analytics_data.csv")
SaveDataAsCSV.df_to_csv_in_dir(dataframe=df2, caller_path=__file__, relative_target_path="../Analytics/Alokeveer", csv_filename="alokeveer_analytics_data.csv")
