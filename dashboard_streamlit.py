import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from utils import convert_mult_format_data, convert_category

path = "./data/dataset_desafio_fadesp.csv"
df = pd.read_csv(path, encoding="latin1", sep=",")

df["Order Date"] = df["Order Date"].apply(convert_mult_format_data)
df["Ship Date"] = df["Ship Date"].apply(convert_mult_format_data)

categories = df.select_dtypes(include="object").columns


def convert_category(df: pd.DataFrame, columns):
    for coluna in columns:
        df[coluna] = df[coluna].astype("category")
    return df


df = convert_category(df, categories)


df["Order Date"] = pd.to_datetime(df["Order Date"])
segment = st.selectbox("Segment", df["Segment"].unique())
region = st.selectbox("Region", df["Region"].unique())
ship_mode = st.selectbox("Category", df["Ship Mode"].unique())
year = st.selectbox("Year", df["Order Date"].dt.year.unique())
month = st.selectbox("Month", df["Order Date"].dt.month.unique())

df_filtered = df[
    (df["Segment"] == segment)
    & (df["Ship Mode"] == ship_mode)
    & (df["Region"] == region)
    & (df["Order Date"].dt.year == year)
    & (df["Order Date"].dt.month == month)
]

sales_date_figure = px.line(df_filtered, x="Order Date", y="Sales")
sales_city_figure = px.bar(df_filtered, x="City", y="Sales")
sales_profit_figure = px.scatter(df_filtered, x="Sales", y="Profit")
sales_shipping_cost_figure = px.line(df_filtered, x="Order Date", y="Shipping Cost")
st.plotly_chart(sales_date_figure)
st.plotly_chart(sales_city_figure)
st.plotly_chart(sales_profit_figure)
st.plotly_chart(sales_shipping_cost_figure)
