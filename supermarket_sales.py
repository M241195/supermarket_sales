import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Supermarket Items Sales",page_icon=':ledger:',layout='wide')
df = pd.read_csv('supermarket_sales.csv')
st.sidebar.header('Filter')

product_sector=st.sidebar.multiselect(
    "Select Product Sector",
    options = df['Product line'].unique(),
    default = df['Product line'].unique()[:3]
)

gender=st.sidebar.multiselect(
    "Select Gender",
    options = df['Gender'].unique(),
    default = df['Gender'].unique()[:2]
)

city=st.sidebar.multiselect(
    "Select City",
    options = df['City'].unique(),
    default = df['City'].unique()[:2]
)

customer_type=st.sidebar.multiselect(
    "Select Customer Type",
    options = df['Customer type'].unique(),
    default = df['Customer type'].unique()[:2]
)

payment=st.sidebar.multiselect(
    "Select Payment Type",
    options = df['Payment'].unique(),
    default = df['Payment'].unique()[:2]
)

st.title(":chart_with_upwards_trend: Supermarket Items Sales Dashboard 2019")
st.markdown("##")
total_sales = df['Total'].sum()
total_profit = df['gross income'].sum()
product_num = df['Product line'].nunique()
left_col,middle_col,right_col = st.columns(3)
with left_col:
    st.subheader('Total Sales')
    st.subheader(f'US $ {total_sales:.2f}')
with middle_col:
    st.subheader('gross income')
    st.subheader(f'US $ {total_profit:.2f}')
with right_col:
    st.markdown(f'<h3 style="text-align: center;">{'Product Sector'}</h3>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="text-align: center;">{product_num}</h3>', unsafe_allow_html=True)
df_select = df.query("City==@city and `Product line`==@product_sector and Gender==@gender and `Customer type`==@customer_type and Payment==@payment")
sales_by_product = df_select.groupby('Product line')['Total'].sum().sort_values(ascending=False)

sales_fig = px.bar(
    sales_by_product,
    x=sales_by_product.values,  
    y=sales_by_product.index,   
    orientation='h',           
    title='Sales by Product',
    labels={'x': 'Total Sales'},
)

a_col,b_col = st.columns(2)
a_col.plotly_chart(sales_fig,use_container_width=True)

sales_by_gender = df_select.groupby('Gender')['Total'].sum().sort_values(ascending=False)

gender_fig = px.bar(
    sales_by_gender,
    x=sales_by_gender.index,  
    y=sales_by_gender.values,   
    orientation='v',           
    title='Sales by Gender',
    labels={'x': 'Total Sales'},
)
b_col.plotly_chart(gender_fig, use_container_width=True)
c_col = st.columns(1)[0]
product_fig = px.pie(
    df_select,
    values = 'gross income',
    names = 'Product line',
    title = 'Profit by Product Sector',
)
c_col.plotly_chart(product_fig,use_container_width=True)

d_col,e_col = st.columns(2)

sales_by_city = df_select.groupby('City')['Total'].sum().sort_values(ascending=False)
city_fig= px.line(
    sales_by_city,
    x = sales_by_city.index,
    y = sales_by_city.values,
    title = 'Sales by City',
    labels={'x': 'City', 'y': 'Total Sales'}
)
d_col.plotly_chart(city_fig, use_container_width=True)

scatter_fig = px.scatter(
    df,
    x = 'Total',
    y = 'Quantity',
    title = ('Total of All Sales')
)
e_col.plotly_chart(scatter_fig, use_container_width=True)

f_col,g_col = st.columns(2)
payment_fig = px.pie(
    df_select,
    values = 'Total',
    names = 'Payment',
    title = 'Sales by Payment Type',
)
f_col.plotly_chart(payment_fig,use_container_width=True)

customertype_fig = px.pie(
    df_select,
    values = 'Total',
    names = 'Customer type',
    title = 'Sales by Customer Type',
)
g_col.plotly_chart(customertype_fig,use_container_width=True)
   
