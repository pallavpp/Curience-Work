try:
    import os
    import pandas
except Exception as e:
    print(e)
    print("Exception encountered while importing modules in Modules/DFtoCSV")

def df_to_csv_in_data(dataframe, caller_path):
    """
    This function should only be used by files present in Scripts/ directory.\n
    It saves the passed DataFrame inside Data/ directory, with same name as the file that calls this function.\n
    \n
    Parameters:\n
    dataframe - Pandas DataFrame to be saved\n
    caller_path - Path of the file calling this function, can be provided using __file__
    """

    csv_filename = os.path.basename(caller_path).split('.')[0] + ".csv"
    csv_path = os.path.abspath(os.path.join(os.path.dirname(caller_path), "../Data", csv_filename))
    dataframe.to_csv(csv_path, index=False)

def dataclass_to_csv_in_data(dataclass_list, column_name_list, caller_path):
    """
    This function should only be used by files present in Scripts/ directory.\n
    It saves the passed dataclass list inside Data/ directory, with same name as the file that calls this function.\n
    \n
    Parameters:\n
    dataclass_list - List of dataclass containing data\n
    column_name_list - List containing column names\n
    caller_path - Path of the file calling this function, can be provided using __file__
    """

    dataframe = pandas.DataFrame(dataclass_list)
    dataframe.columns = column_name_list
    csv_filename = os.path.basename(caller_path).split('.')[0] + ".csv"
    csv_path = os.path.abspath(os.path.join(os.path.dirname(caller_path), "../Data", csv_filename))
    dataframe.to_csv(csv_path, index=False)
