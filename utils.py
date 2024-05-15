import sqlite3
import os
import pandas as pd


def convert_multi_format_data(date_str):
    """tenta converter primeiramente o formato de string '%m/%d/%Y' para datetime, caso tenha erro,
    a função lida com esse erro atribuindo a conversão do formato '%d-%m-%Y' para datetime. nesse caso serve para ambas
    as colunas.
    """
    try:
        return pd.to_datetime(date_str, format="%m/%d/%Y")
    except ValueError:
        return pd.to_datetime(date_str, format="%d-%m-%Y")


def salva_tabela(df, table_name, db):
    with sqlite3.connect(db) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    return True


def carrega_df(query, db=None):
    """carrega dataframe a partir de query, se db não especificado, será usado o db padão que está na pasta."""
    if db is None:
        arquivos = os.listdir()
        arquivos_db = [arquivo for arquivo in arquivos if arquivo.endswith(".db")]
        try:
            if not arquivos_db:
                raise FileNotFoundError(
                    "Nenhum arquivo de banco de dados '.db' foi encontrado na pasta atual."
                )
            db = arquivos_db[0]
        except FileNotFoundError as e:
            print(e)
            return None
    try:
        with sqlite3.connect(db) as conn:
            df = pd.read_sql_query(query, conn)
        return df

    except sqlite3.Error as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        return None


def convert_category(df: pd.DataFrame, columns):
    for coluna in columns:
        df[coluna] = df[coluna].astype("category")
    return df
