import os
import pandas

# saving in given directory
def df_to_csv_in_dir(dataframe, caller_path, relative_target_path, csv_filename=None):
    """
    Saves the passed DataFrame inside target directory, with provided filename or caller's name as default.\n
    \n
    Parameters:\n
    dataframe - Pandas DataFrame to be saved\n
    caller_path - Path of the file calling this function, can be provided using __file__\n
    relative_target_path - Target directory path relative to caller path directory, provide as a string\n
    csv_filename (optional) - File name to be used, provide along with filename extension.
    """

    if csv_filename == None:
        csv_filename = os.path.basename(caller_path).split('.')[0] + ".csv"
    csv_path = os.path.abspath(os.path.join(os.path.dirname(caller_path), relative_target_path, csv_filename))
    target_directory = os.path.dirname(csv_path)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    dataframe.to_csv(csv_path, index=False)

# saving in same directory
def df_to_csv_in_currdir(dataframe, caller_path, csv_filename=None):
    """
    Saves the passed DataFrame inside same directory, with provided filename or caller's name as default.\n
    \n
    Parameters:\n
    dataframe - Pandas DataFrame to be saved\n
    caller_path - Path of the file calling this function, can be provided using __file__\n
    csv_filename (optional) - File name to be used, provide along with filename extension.
    """

    if csv_filename == None:
        csv_filename = os.path.basename(caller_path).split('.')[0] + ".csv"
    csv_path = os.path.abspath(os.path.join(os.path.dirname(caller_path), csv_filename))
    target_directory = os.path.dirname(csv_path)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    dataframe.to_csv(csv_path, index=False)

def dataclass_to_csv_in_currdir(dataclass_list, column_name_list, caller_path, csv_filename=None):
    """
    Saves the passed dataclass inside same directory, with provided filename or caller's name as default.\n
    \n
    Parameters:\n
    dataclass_list - List of dataclass containing data\n
    column_name_list - List containing column names\n
    caller_path - Path of the file calling this function, can be provided using __file__\n
    csv_filename (optional) - File name to be used, provide along with filename extension
    """

    dataframe = pandas.DataFrame(dataclass_list)
    dataframe.columns = column_name_list
    if csv_filename == None:
        csv_filename = os.path.basename(caller_path).split('.')[0] + ".csv"
    csv_path = os.path.abspath(os.path.join(os.path.dirname(caller_path), csv_filename))
    target_directory = os.path.dirname(csv_path)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    dataframe.to_csv(csv_path, index=False)

# saving data in 'Data' directory
def df_to_csv_in_data(dataframe, caller_path, csv_filename=None):
    """
    Saves the passed DataFrame inside 'Data' directory, with provided filename or caller's name as default.\n
    \n
    Parameters:\n
    dataframe - Pandas DataFrame to be saved\n
    caller_path - Path of the file calling this function, can be provided using __file__\n
    csv_filename (optional) - File name to be used, provide along with filename extension
    """

    if csv_filename == None:
        csv_filename = os.path.basename(caller_path).split('.')[0] + ".csv"
    csv_path = os.path.abspath(os.path.join(os.path.dirname(caller_path), "../Data", csv_filename))
    target_directory = os.path.dirname(csv_path)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    dataframe.to_csv(csv_path, index=False)

def dataclass_to_csv_in_data(dataclass_list, column_name_list, caller_path, csv_filename=None):
    """
    Saves the passed dataclass list inside 'Data' directory, with provided filename or caller's name as default.\n
    \n
    Parameters:\n
    dataclass_list - List of dataclass containing data\n
    column_name_list - List containing column names\n
    caller_path - Path of the file calling this function, can be provided using __file__\n
    csv_filename (optional) - File name to be used, provide along with filename extension
    """

    dataframe = pandas.DataFrame(dataclass_list)
    dataframe.columns = column_name_list
    if csv_filename == None:
        csv_filename = os.path.basename(caller_path).split('.')[0] + ".csv"
    csv_path = os.path.abspath(os.path.join(os.path.dirname(caller_path), "../Data", csv_filename))
    target_directory = os.path.dirname(csv_path)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    dataframe.to_csv(csv_path, index=False)
