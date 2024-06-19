import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from warnings import filterwarnings
filterwarnings('ignore')

# Read csv file
def dataframe():
    df = pd.read_csv("RiceExport_Final.csv")
    return df

with st.sidebar:
        SELECT = option_menu(None,
                options = ["🏡Home","🌍Data Insights","🔚Exit"],
                default_index=0,
                orientation="vertical",
                styles={"container": {"width": "90%"},
                        "icon": {"color": "white", "font-size": "18px"},
                        "nav-link": {"font-size": "18px"}})
        
if SELECT == '🏡Home':
    st.header("**_Introduction to Rice Export Data Analysis:_**")
    st.markdown("""
    Welcome to the Comprehensive Rice Export Data Analysis tool! This platform is 
                designed to provide valuable insights into the intricate world 
                of rice exports,featuring a rich dataset with detailed 
                information on transactions between exporters and importers worldwide.""")

    st.markdown("""
    Our dataset encapsulates crucial attributes such as importer/exporter names, addresses, 
                quantities, values, and other pertinent details. The goal of this analysis 
                is to delve into this extensive dataset, uncover meaningful patterns, 
                and address key questions surrounding rice export transactions.""")

    st.subheader("**Key Objectives:**")

    st.markdown("""
    1. **In-depth Exploration:**
       Uncover hidden patterns and trends within the dataset to gain a comprehensive understanding of global rice export dynamics.

    2. **Insightful Analysis:**
        Extract meaningful insights that can aid decision-makers in the rice industry, be it exporters, importers, or stakeholders.

    3. **Key Questions Addressed:**
        Tackle crucial questions regarding the rice export landscape, such as market trends, top exporters, notable importers, and the overall economic impact.
    """)
    st.subheader("**Tools Used:**")
    st.markdown("""
        - **_Python:_** Facilitates versatile programming capabilities.
        - **_Pandas:_** Refines and prepares data for accurate analysis.
        - **_Matplotlib:_** Crafts static visualizations to uncover trends.
        - **_Plotly:_** Creates dynamic and interactive visual displays.
        - **_Streamlit:_** Enables the development of a user-friendly web application for exploring Airbnb data.
        """)

if SELECT == "🌍Data Insights":
    option=st.sidebar.selectbox("**Select Any One Option:**", (None,'Data Acquisition','Geographical Details','Importer/Exporters Highlights','Product Analysis','Financial Analysis','Time Series Analysis'))
    if option=="Data Acquisition":
           st.subheader("**_Pre-Processed DataFrame_**")
           df = dataframe()
           st.dataframe(df)
    if option == "Geographical Details":
        df = dataframe()
        df_concode = df.groupby(['IMPORTER COUNTRY']).agg({'IMPORT VALUE FOB': 'mean','IMPORT VALUE CIF':'mean'}).reset_index()
        fig = px.scatter_geo(data_frame=df_concode,
                    locations='IMPORTER COUNTRY',
                    color= 'IMPORT VALUE CIF', 
                    hover_data=['IMPORT VALUE FOB','IMPORT VALUE CIF'],
                    locationmode='country names',
                    color_continuous_scale='earth',
                    title= 'Total Value Of The Imported Rice Based On Contries')
        fig.update_geos(bgcolor='#A0C1B0')
        st.plotly_chart(fig,use_container_width=True)

        df_concode = df.groupby(['PORT OF ARRIVAL']).agg({'IMPORT VALUE FOB': 'mean','IMPORT VALUE CIF':'mean'}).reset_index()
        fig = px.scatter_geo(data_frame=df_concode,
                    locations='PORT OF ARRIVAL',
                    color= 'IMPORT VALUE FOB', 
                    hover_data=['IMPORT VALUE FOB'],
                    locationmode='country names',
                    color_continuous_scale='earth',
                    title= 'Port Of Arival Based On Value Of Imported Value')
        fig.update_geos(bgcolor='#A0C1B0')
        st.plotly_chart(fig,use_container_width=True)
    

        df_concode = df.groupby(['PORT OF DEPARTURE']).agg({'IMPORT VALUE FOB': 'mean','IMPORT VALUE CIF':'mean'}).reset_index()
        fig = px.scatter_geo(data_frame=df_concode,
                    locations='PORT OF DEPARTURE',
                    color= 'IMPORT VALUE FOB', 
                    hover_data=['IMPORT VALUE FOB'],
                    locationmode='country names',
                    color_continuous_scale='earth',
                    title= 'Port Of Departure Based On Value Of Imported Value')
        fig.update_geos(bgcolor='#A0C1B0')
        st.plotly_chart(fig,use_container_width=True)

    if option == 'Importer/Exporters Highlights':
        df = dataframe()
        tab1,tab2=st.tabs(["**_Importers Insights_**","**_Exporters Insights_**"])
        with tab1:
            st.subheader("**_Importers Information!_**")
            country = st.selectbox('Select a Country',(None,sorted(df['IMPORTER COUNTRY'].unique())))
            button=st.button("Click Me To Get More Details!")
            if button:               
                df1=df[(df["IMPORTER COUNTRY"] == country)]
                df2=df1[["IMPORTER COUNTRY","IMPORTER NAME","IMPORT VALUE FOB","CURRENCY","PORT OF ARRIVAL"]].reset_index(drop=True)
                st.dataframe(df2)

                st.subheader("**_Top Importers_**")
                fig = px.bar(df['IMPORTER NAME'].value_counts().head(10), orientation='h')
                fig.update_traces(marker_color='#577765')
                fig.update_layout(width=10,height=500,title_text='Top 10 Importer Names')   
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("**_Imported Quantity Details!_**")
            name = st.selectbox('Select a Importer',(None,sorted(df['IMPORTER NAME'].unique())))
            button=st.button(("Click Me To Get More Details!"),key ="button1")
            if button:               
                df1=df[(df["IMPORTER NAME"] == name)]
                df2=df1[["IMPORTER NAME","IMPORT VALUE FOB","QUANTITY","QUANTITY UNIT"]].reset_index(drop=True)
                st.dataframe(df2)
        with tab2:
            st.subheader("**_Exporters Information!_**")
            exportname = st.selectbox('Select Country',(None,sorted(df['EXPORTER NAME'].unique())))
            button=st.button(("Click Me To Get More Details!"),key ="button2")
            if button:               
                df3=df[(df["EXPORTER NAME"] == exportname)]
                df4=df3[["COUNTRY OF ORIGIN","EXPORTER NAME","QUANTITY","QUANTITY UNIT","HS CODE","PRODUCT DETAILS","PORT OF DEPARTURE"]].reset_index(drop=True)
                st.dataframe(df4)

                st.subheader("**_Top Exporters_**")
                fig = px.bar(df['EXPORTER NAME'].value_counts().head(10), orientation='h')
                fig.update_traces(marker_color='#577765')
                fig.update_layout(width=10,height=500,title_text='Top 10 Importer Names')   
                st.plotly_chart(fig, use_container_width=True)

    if option == "Product Analysis":
        df = dataframe()
        st.subheader("**_Overall Anlysis Of Product!_**")
        name = st.selectbox('Select a Product',(None,sorted(df['PRODUCT DETAILS'].unique())))
        button=st.button(("Click Me To Get More Details!"),key ="button4")
        if button:               
            df1=df[(df["PRODUCT DETAILS"] == name)]
            df2=df1[["IMPORTER NAME","IMPORTER COUNTRY","HS CODE","PRODUCT DETAILS","QUANTITY","QUANTITY UNIT"]].reset_index(drop=True)
            st.dataframe(df2)

        st.subheader("**_Top Product_**")
        fig = px.bar(df['PRODUCT DETAILS'].value_counts().head(10))
        fig.update_traces(marker_color='#577765')
        fig.update_layout(width=10,height=700,title_text='Top 10 Rice Varieties')   
        st.plotly_chart(fig, use_container_width=True)

    if option == "Financial Analysis":
        df = dataframe()
        st.subheader("**_Overall Analysis Of Product!_**")
        name = st.selectbox('Select a Country',(None,sorted(df['IMPORTER COUNTRY'].unique())))
        button=st.button(("Click Me To Get More Details!"),key ="button4")
        if button:               
            df1=df[(df["IMPORTER COUNTRY"] == name)]
            f_concode = df1.groupby(['IMPORTER COUNTRY']).agg({'IMPORT VALUE FOB': 'sum'}).reset_index().head(10)
            st.dataframe(f_concode)


        st.subheader("**_Total Trascation Amount By Impoters!_**")
        f_concode = df.groupby(['IMPORTER COUNTRY']).agg({'IMPORT VALUE FOB': 'sum'}).reset_index().head(10)
        fig = px.pie(f_concode, names="IMPORTER COUNTRY", values="IMPORT VALUE FOB", title="Top 10 Countries With High Trasaction Amount",
                    hole=0.3)
        fig.update_layout(piecolorway=["#577765"])
        fig.update_traces(textposition='inside', textinfo='label+percent')
        fig.update_layout(width=300, height=400)
        st.plotly_chart(fig,use_container_width=True)

    if option=="Time Series Analysis":
        df = dataframe()
        st.subheader("**_Total Quantity Of Rice Exported Based On Year!_**")
        df['ARRIVAL DATE'] = pd.to_datetime(df['ARRIVAL DATE'])
        f_concode = df.groupby([df['ARRIVAL DATE'].dt.year]).agg({'QUANTITY': 'sum'}).reset_index().sort_values(by="QUANTITY",ascending=False)
        fig = px.pie(f_concode, names= 'ARRIVAL DATE', values="QUANTITY", title="Total Quantity Of Rice Exported",
                    hole=0.3)
        fig.update_layout(piecolorway=["#577765"])
        fig.update_traces(textposition='inside', textinfo='label+percent')
        fig.update_layout(width=300, height=400)
        st.plotly_chart(fig,use_container_width=True) 


        st.subheader("**_Total Quantity Of Rice Exported Based On Day!_**")
        df['ARRIVAL DATE'] = pd.to_datetime(df['ARRIVAL DATE'])
        f_concode = df.groupby([df['ARRIVAL DATE'].dt.day]).agg({'QUANTITY': 'mean'}).reset_index().sort_values(by="QUANTITY",ascending=False)
        f_concode = f_concode.reset_index(drop=True)
        fig = px.bar(f_concode, x="ARRIVAL DATE", y="QUANTITY", title="Total Quantity Vs Days",
                            hover_data = ['ARRIVAL DATE','QUANTITY'])
        fig.update_traces(marker_color='#577765') 
        fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'))
        fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'))
        fig.update_layout(width=10,height=500)
        st.plotly_chart(fig,use_container_width=True)

if SELECT == "🔚Exit":
    st.subheader("**_Conclusion_**")
    st.markdown("""Performed comprehensive analysis on a global rice export dataset, addressing missing values, 
                outliers, and ensuring data consistency. Utilized descriptive statistics, visualizations, and 
                geospatial analysis to identify key insights. Explored trends over time, correlations between 
                variables, and geographical patterns. Concluded with actionable recommendations based on the findings.""")
    but = st.button("Exit!")
    if but:
          st.success("Thank You For Utilising This Platform. I Hope This User Interface Provided You With Some Insightful Data!❤️")

    
                
