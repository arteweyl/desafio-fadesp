import streamlit as st
import pandas as pd
import plotly.express as px
from utils import convert_multi_format_data, convert_category


path = './data/dataset_desafio_fadesp.csv'
df = pd.read_csv(path, encoding='latin1', sep=',')

df['Order Date']= df['Order Date'].apply(convert_multi_format_data)
df['Ship Date']=df['Ship Date'].apply(convert_multi_format_data)

categories = df.select_dtypes(include= 'object').columns

def convert_category(df: pd.DataFrame, colunas):
    for coluna in colunas:
        df[coluna] = df[coluna].astype('category')
    return df

df = convert_category(df, categories)

# Converte 'Order Date' para datetime e extrai o mês e o ano
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Cria os filtros
segment = st.selectbox('Segment', df['Segment'].unique())
region = st.selectbox('Region', df['Region'].unique())
category = st.selectbox('Category', df['Category'].unique())

df_filtered = df[(df['Segment'] == selected_segment) &
                 (df['Region'] == selected_region) &
                 (df['Category'] == selected_category) &
                 #(df['Order Priority'] == selected_priority) &
                 (df['YearMonth'] == selected_yearmonth)]

# Cria os gráficos
sales_date_figure = px.line(df_filtered, x='Order Date', y='Sales')
sales_region_figure = px.bar(df_filtered, x='Region', y='Sales')
sales_profit_figure = px.scatter(df_filtered, x='Sales', y='Profit')
st.plotly_chart(sales_date_figure)
st.plotly_chart(sales_region_figure)
st.plotly_chart(sales_profit_figure)