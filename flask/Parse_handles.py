import pandas as pd

def parse_handles():

    # Load CSV into a DataFrame
    df = pd.read_csv(
        "../popular_channel_handles.txt",
        delimiter=",",  # custom delimiter (default is ",")
        header=0,  # row number to use as column names
        skiprows=1,  # skip first row(s)
        names=["channel", "handle", "relation"],  # custom column names
        usecols=[0, 1],  # read only certain columns
        na_values=["NA", ""],  # treat these as missing values
    )

    

    handles = df["handle"].tolist()
    print(handles)
