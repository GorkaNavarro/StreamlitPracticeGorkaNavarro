import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(layout="wide")

st.title("Gorka Navarro Navarro")

df = pd.read_csv("C:/ICADE/DataViz/airbnb.csv")

option = st.sidebar.selectbox('Choose a function:',['Home','Listing type - Number of bookings\nCorrelation graph','Reviews - Price graph by Neigbourhood Group','Plot your own graphic'],index=0) #The index 0 thing is so that the default option when the page refreshes is Home

if option == "Home":
    tab1, tab2 = st.tabs(["Home", "DataFrame viewer"])
    with tab1:     
        st.header("Welcome! This is my Streamlit Practice!" )
        st.subheader("By: Gorka Navarro Navarro, 2ºE8")
        st.text("The data used in this practice comes from this .csv file:")
        st.write(df.head(5))
        st.text("(Preview of the first 5 rows)")

    with tab2:
        columns_list = df.columns.tolist()
        columns = st.multiselect('Select which columns to view:', options=columns_list)

        if columns:
            st.write(df[columns])
        else:
            st.write("Select which columns to view:")

elif option == "Listing type - Number of bookings\nCorrelation graph":
    lower_fig1 = df['number_of_reviews'].quantile(0.05)
    upper_fig1 = df['number_of_reviews'].quantile(0.95)
    df_fig1 = df[(df['number_of_reviews'] <= upper_fig1) & (df['number_of_reviews'] >= lower_fig1)]

    df_fig1['booked_days'] = 365 - df['availability_365']

    fig1 = px.density_heatmap(df_fig1, x='booked_days', y='number_of_reviews',nbinsx = 45, nbinsy=20 ,hover_name="name", title = "Listing type - Number of bookings Correlation heatmap"
    )
    st.plotly_chart(fig1)

elif option == "Reviews - Price graph by Neigbourhood Group":
    lower_fig2 = df['price'].quantile(0.05)
    upper_fig2 = df['price'].quantile(0.95)
    df_fig2 = df[(df['price'] <= upper_fig2) & (df['price'] >= lower_fig2)]

    neigh_options = df['neighbourhood_group'].unique()

    neigh_option = st.selectbox('Choose an neighbourhood group:', neigh_options)

    st.write(neigh_option)

    df_fig2["reviews_per_month"].fillna(0, inplace = True)

    neigh_df = df_fig2[df_fig2['neighbourhood_group'] == neigh_option]

   

    fig2 = px.scatter(neigh_df, x='price', y='number_of_reviews', color='neighbourhood_group', size_max=20,size="reviews_per_month",
        hover_name="name", title = "Reviews - Price graph by Neigbourhood Group"
        )
    st.plotly_chart(fig2)

elif option == "Plot your own graphic":
    col1, col2 = st.columns(2)
    with col1:
        x_option = st.radio("Select the x axis:", ["price","minimum_nights","number_of_reviews","reviews_per_month","calculated_host_listings_count","availability_365"])
    
    with col2:
        y_option = st.radio("Select the y axis:",["price","minimum_nights","number_of_reviews","reviews_per_month","calculated_host_listings_count","availability_365"])

    lower_fig3_x = df[x_option].quantile(0.05)
    upper_fig3_x = df[x_option].quantile(0.95)
    df_fig3 = df[(df[x_option] <= upper_fig3_x) & (df[x_option] >= lower_fig3_x)]

    lower_fig3_y = df[y_option].quantile(0.05)
    upper_fig3_y = df[y_option].quantile(0.95)
    df_fig3 = df[(df[y_option] <= upper_fig3_y) & (df[y_option] >= lower_fig3_y)]

    fig3 = px.scatter(df_fig3, x=x_option, y=y_option, color='neighbourhood_group', size_max=20,
                 hover_name="name", title = ("Plot of: " + x_option + " and " + y_option)
    )
    st.plotly_chart(fig3)