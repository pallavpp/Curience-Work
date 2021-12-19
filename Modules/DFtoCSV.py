def df_to_csv(df):
    csv_filename = os.path.basename(__file__).split('.')[0] + ".csv"
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Data", csv_filename))
    df.to_csv(csv_path, index=False)
