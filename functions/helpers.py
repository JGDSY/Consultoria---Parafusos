import pandas as pd

def get_df(uploaded_file = None):
    if uploaded_file is None:
        csv_file = "dados_vins.csv"
        df = pd.read_csv(csv_file)
    else:
        df = pd.read_csv(uploaded_file)
    df['phantom']=df['phantom'].astype(str)

    return df

def columns_are_not_ok(df):
    is_columns_ok = all([col in df.columns for col in ["X","phantom","vin","PN","Qtde","Price"]])

    return not is_columns_ok
