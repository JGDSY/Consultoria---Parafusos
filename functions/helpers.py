import pandas as pd

def get_df(uploaded_file = None):
    if uploaded_file is None:
        csv_file = "dados_vins.csv"
        df = pd.read_csv(csv_file)
    else:
        df = pd.read_csv(uploaded_file)
    df['phantom']=df['phantom'].astype(str)

    return df
