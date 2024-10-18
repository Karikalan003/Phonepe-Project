import streamlit as st 
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import json
import requests 
from streamlit_elements import elements, mui, html, sync
import base64
import time


#Data Frame Creation

mydb = psycopg2.connect(
        host="localhost",
        user="postgres",      
        password="hari",
        database="Phonepe Pulse Data Visualization and Exploration",
        port="5432"
)

cursor = mydb.cursor()

#Aggregated_Insurance_DF

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall() #fetching all the data

Aggregated_Insurance_DF = pd.DataFrame(table1, columns = ("State", "Year","Quarter", 
                                                            "Transaction_Type" , "Transaction_Count" , 
                                                            "Transaction_Amount"
))

#Aggregated_Transaction_DF

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall() #fetching all the data

Aggregated_Transaction_DF = pd.DataFrame(table2, columns = ("State", "Year","Quarter", 
                                                            "Transaction_Type" , 
                                                            "Transaction_Count" , 
                                                            "Transaction_Amount"
))

#Aggregated_User_DF

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3 = cursor.fetchall() #fetching all the data

Aggregated_User_DF = pd.DataFrame(table3, columns = ("State", "Year","Quarter", 
                                                            "Brand" , 
                                                            "Transaction_Count" , 
                                                            "Percentage"
))

#Map_Insurance_DF

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4 = cursor.fetchall() #fetching all the data

Map_Insurance_DF = pd.DataFrame(table4, columns = ("State", "Year","Quarter", 
                                                            "District_Name" , 
                                                            "Transaction_Count" , 
                                                            "Transaction_Amount"
))

#Map_Transaction_DF

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5 = cursor.fetchall() #fetching all the data

Map_Transaction_DF = pd.DataFrame(table5, columns = ("State", "Year","Quarter", 
                                                            "District_Name" , 
                                                            "Transaction_Count" , 
                                                            "Transaction_Amount"
))

#Map_User_DF

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6 = cursor.fetchall() #fetching all the data

Map_User_DF = pd.DataFrame(table6, columns = ("State", "Year","Quarter", 
                                                            "District_Name" , 
                                                            "Registered_User" , 
                                                            "App_Open_Count"
))

#Top_Insurance_DF

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7 = cursor.fetchall() #fetching all the data

Top_Insurance_DF = pd.DataFrame(table7, columns = ("State", "Year","Quarter", 
                                                            "Pincode" , 
                                                            "Transaction_Count" , 
                                                            "Transaction_Amount"
))

#Top_Transaction_DF

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8 = cursor.fetchall() #fetching all the data

Top_Transaction_DF = pd.DataFrame(table8, columns = ("State", "Year","Quarter", 
                                                            "Pincode" , 
                                                            "Transaction_Count" , 
                                                            "Transaction_Amount"
))

#Top_User_DF

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9 = cursor.fetchall() #fetching all the data

Top_User_DF = pd.DataFrame(table9, columns = ("State", "Year","Quarter", 
                                                            "Pincode" , 
                                                            "Registered_User"
))



#Aggregated_Insurance_Yearwise
def a_i_a_c_y(df, year):
    #a_i_a_c_y = Aggregated_Insurance_Amount_Count_Yearwise, AIACYG = Aggregated_Insurance_Amount_Count_Yearwise_Grouping

    AIACY = df[df["Year"] == year]
    AIACY.reset_index(drop = True , inplace = True)

    AIACYG = AIACY.groupby("State")[["Transaction_Count","Transaction_Amount"]].sum() # getting sum values of the count and amount according to state in 2021
    AIACYG.reset_index(inplace = True) #missligned "State" column rectified by using

    col1, col2 = st.columns(2)
    with col1:

        fig_count = px.bar(AIACYG, x = "State", y = "Transaction_Count", 
                        title = f"TRANSACTION COUNT {AIACY['Year'].unique()}", color_discrete_sequence= px.colors.sequential.Magenta_r,height=650, width = 600)
        st.plotly_chart(fig_count)

    with col2:

        fig_amount = px.bar(AIACYG, x = "State", y = "Transaction_Amount", 
                            title = f"TRANSACTION AMOUNT {AIACY['Year'].unique()}", color_discrete_sequence= px.colors.sequential.Greens_r, height=650, width = 600)
        st.plotly_chart(fig_amount)


    col1, col2 = st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url)
        data1 = json.loads(response.content)

        State_Name = []

        for feature in data1["features"]:
            State_Name.append(feature["properties"]["ST_NM"])

        State_Name.sort()

        fig_india_1 = px.choropleth(AIACYG,geojson=data1, locations= "State", 
                                    featureidkey= "properties.ST_NM", color= "Transaction_Count",
                                    color_continuous_scale= "Plasma", 
                                    range_color= (AIACYG ["Transaction_Count"].min(),AIACYG ["Transaction_Count"].max()),
                                    hover_name= "State", title= f"TRANSACTION COUNT {AIACY['Year'].unique()}", 
                                    fitbounds= "locations", height=650, width = 600 
        )
        
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2 = px.choropleth(AIACYG,geojson=data1, locations= "State", 
                                featureidkey= "properties.ST_NM", color= "Transaction_Amount",
                                color_continuous_scale= "Plasma", 
                                range_color= (AIACYG ["Transaction_Amount"].min(),AIACYG ["Transaction_Amount"].max()),
                                hover_name= "State", title= f"TRANSACTION AMOUNT {AIACY['Year'].unique()}", 
                                fitbounds= "locations", height=650, width = 600 
        )
        
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return AIACY


#Aggregated_Insurance_Quarterwise
def a_i_a_c_y_q(df, quarter):
    #a_i_a_c_y_q - aggregated_insurance_amount_count_Year_Quarterwise
  

    AIACY = df[df["Quarter"] == quarter]
    AIACY.reset_index(drop = True , inplace = True)

    AIACYG = AIACY.groupby("State")[["Transaction_Count","Transaction_Amount"]].sum() # getting sum values of the count and amount according to state in 2021
    AIACYG.reset_index(inplace = True) #missligned "State" column rectified by using

    col1,col2 = st.columns(2)

    with col1:

        fig_count = px.bar(AIACYG, x = "State", y = "Transaction_Count", 
                        title = f"TRANSACTION COUNT {AIACY['Year'].unique()} - QUARTER:{quarter}", color_discrete_sequence= px.colors.sequential.Magenta_r, height=650, width = 600)
        st.plotly_chart(fig_count)

    with col2:

        fig_amount = px.bar(AIACYG, x = "State", y = "Transaction_Amount", 
                            title = f"TRANSACTION AMOUNT {AIACY['Year'].unique()} - QUARTER:{quarter}", color_discrete_sequence= px.colors.sequential.Greens_r, height=650, width = 600)
        st.plotly_chart(fig_amount) #We can use "min" or "max" instead of "unique" to remove the list bracket


    col1,col2 = st.columns(2)

    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url)
        data1 = json.loads(response.content)

        State_Name = []

        for feature in data1["features"]:
            State_Name.append(feature["properties"]["ST_NM"])

        State_Name.sort()

        fig_india_1 = px.choropleth(AIACYG,geojson=data1, locations= "State", 
                                    featureidkey= "properties.ST_NM", color= "Transaction_Count",
                                    color_continuous_scale= "Plasma", 
                                    range_color= (AIACYG ["Transaction_Count"].min(),AIACYG ["Transaction_Count"].max()),
                                    hover_name= "State", title= f"TRANSACTION COUNT {AIACY['Year'].unique()} - QUARTER:{quarter}", 
                                    fitbounds= "locations", height=650, width = 600 
        )
        
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2 = px.choropleth(AIACYG,geojson=data1, locations= "State", 
                                featureidkey= "properties.ST_NM", color= "Transaction_Amount",
                                color_continuous_scale= "Plasma", 
                                range_color= (AIACYG ["Transaction_Amount"].min(),AIACYG ["Transaction_Amount"].max()),
                                hover_name= "State", title= f"TRANSACTION AMOUNT {AIACY['Year'].unique()} - QUARTER:{quarter}", 
                                fitbounds= "locations", height=650, width = 600 
        )
        
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return AIACY


#Aggregated_Transaction_Transactiontype_Statewise
def a_t_a_c_t_s(df, State):
    #a_t_a_c_t_s = Aggregated_Amount_Count_Transaction_Transactiontype_Statewise


    ATACTS = df[df["State"] == State]
    ATACTS.reset_index(drop = True , inplace = True)

    ATACTSG = ATACTS.groupby("Transaction_Type")[["Transaction_Count","Transaction_Amount"]].sum() 
    ATACTSG.reset_index(inplace = True) 

    col1,col2 = st.columns(2)

    with col1:

        fig_pie_1 = px.pie(data_frame= ATACTSG, names= "Transaction_Type", values= "Transaction_Count",
                                        width= 600, title= f"TRANSACTION COUNT {ATACTS['Year'].unique()} - {State.upper()}", hole = 0.3)

        st.plotly_chart(fig_pie_1)
    
    with col2:

        fig_pie_2 = px.pie(data_frame= ATACTSG, names= "Transaction_Type", values= "Transaction_Amount",
                                        width= 600, title= f"TRANSACTION AMOUNT {ATACTS['Year'].unique()} - {State.upper()}", hole = 0.3)

        st.plotly_chart(fig_pie_2)

    return ATACTS

def a_u_b_a_y(df,year):

    #a_u_b_a_y_q - Aggregated_User_Brand_Amount_Year_Quarterwise

    AUBAY = df[df["Year"] == year]
    AUBAY.reset_index(drop = True, inplace = True)

    AUBAYG = pd.DataFrame(AUBAY.groupby("Brand")["Transaction_Count"].sum())
    AUBAYG.reset_index(inplace = True)

    fig_bar_1 = px.bar(AUBAYG, x = "Brand", y = "Transaction_Count", 
                        title = f"TRANSACTION COUNT - SMARTPHONE BRANDWISE {[year]}",
                        width = 1000, color_discrete_sequence= px.colors.sequential.Burg_r, hover_name= "Brand") 

    st.plotly_chart(fig_bar_1)  

    return AUBAY

 
def a_u_b_a_y_s(df,state):

    #a_u_b_a_y_s = Aggregated_User_Brand_Amount_Year_Statewise

    AUBAYS = df[df["State"] == state]
    AUBAYS.reset_index(drop = True, inplace= True)

    fig_line_1 =  px.line(AUBAYS, x = "Brand", y = "Transaction_Count", hover_data= ["Percentage"],
                        title = f"BRAND, TRANSACTION COUNT & PERCENTAGE {AUBAYS['Year'].unique()} - [{state.upper()}]", 
                        color_discrete_sequence=px.colors.sequential.Burgyl_r,
                        width = 1000, markers = True 
    )
    st.plotly_chart(fig_line_1)

    return AUBAYS


#Aggregated_User_Quarter_Brandwise
def a_u_b_a_y_q(df,quarter):
    #a_u_b_a_y_q - Aggregated_User_Brand_Amount_Year_Quarterwise
   
    AUBAYQ = df[df["Quarter"] == quarter]
    AUBAYQ.reset_index(drop = True, inplace = True)

    AUBAYQG = pd.DataFrame(AUBAYQ.groupby("Brand")["Transaction_Count"].sum())
    AUBAYQG.reset_index(inplace = True)

    fig_bar_1 = px.bar(AUBAYQG, x = "Brand", y = "Transaction_Count", 
                        title = f"TRANSACTION COUNT - SMARTPHONE BRANDWISE {AUBAYQ['Year'].unique()} [QUARTER-{quarter}]",
                        width = 1000, color_discrete_sequence= px.colors.sequential.Burg_r, hover_name= "Brand"
    ) 

    st.plotly_chart(fig_bar_1)

    return AUBAYQ


def m_i_a_c_y_s(df, State):
    #miacys = Map_Insurance_Amount_count_Transactiontype_Statewise
  

    MIACYS = df[df["State"] == State]
    MIACYS.reset_index(drop = True , inplace = True)

    MIACYSG = MIACYS.groupby("District_Name")[["Transaction_Count","Transaction_Amount"]].sum() 
    MIACYSG.reset_index(inplace = True) 

    col1,col2 = st.columns(2)

    with col1:

        fig_bar_1 = px.bar(data_frame= MIACYSG, x = "Transaction_Count", y = "District_Name",orientation= "h",
                                        title= f"TRANSACTION COUNT {MIACYS ['Year'].unique()} - {State.upper()}",height = 700,
                                        color_discrete_sequence= px.colors.sequential.Magenta_r
        )

        st.plotly_chart(fig_bar_1)
    
    with col2:

        fig_bar_2 = px.bar(data_frame= MIACYSG, x = "Transaction_Amount", y = "District_Name",orientation= "h",
                                        title= f"TRANSACTION AMOUNT {MIACYS ['Year'].unique()} - {State.upper()}",height = 700,
                                        color_discrete_sequence= px.colors.sequential.Greens_r
        )

        st.plotly_chart(fig_bar_2)

    return MIACYS



#Map_User_Registereduser_Appopencount_Yearly

def m_u_r_a_y(df, year):

    MURAY = df[df["Year"] == year]
    MURAY.reset_index(drop=True, inplace=True)

    MURAYG = MURAY.groupby("State")[["Registered_User", "App_Open_Count"]].sum()
    MURAYG.reset_index(inplace=True)
    
    fig_line_1 = px.line(MURAYG, x="State", y=["Registered_User","App_Open_Count"],
                        title=f"REGISTERED USER {[year]}",
                        width = 1200,height=800, markers= True,
                        color_discrete_map= {"Registered_User":"green", "App_Open_Count":"blue"}
    )
    
    st.plotly_chart(fig_line_1)  # Use this to display the chart

    return MURAY


def m_u_r_a_y_s(df, State):
    #m_u_r_a_y_s = ap_User_Registereduser_Appopencount_Yearly_State

    MURAYS = df[df["State"] == State]
    MURAYS.reset_index(drop = True , inplace = True)

    MURAYSG = MURAYS.groupby("District_Name")[["Registered_User","App_Open_Count"]].sum() 
    MURAYSG.reset_index(inplace = True) 

    col1,col2 = st.columns(2)

    with col1:

        fig_bar_1 = px.bar(data_frame= MURAYSG, x = "Registered_User", y = "District_Name",orientation= "h",
                                        title= f"REGISTERED USER {MURAYS['Year'].unique()} - {State.upper()}",
                                        color_discrete_sequence= px.colors.sequential.Magenta_r
        )

        st.plotly_chart(fig_bar_1)
    
    with col2:

        fig_bar_2 = px.bar(data_frame= MURAYSG, x = "App_Open_Count", y = "District_Name",orientation= "h",
                                        title= f"APP OPEN COUNT {MURAYS['Year'].unique()} - {State.upper()}",
                                        color_discrete_sequence= px.colors.sequential.Greens_r
        )

        st.plotly_chart(fig_bar_2)

    return MURAYS



#Map_User_Registereduser_Appopencount_Yearly_Quarterly

def m_u_r_a_y_q(df, quarter):
    #m_u_r_a_y_q = Map_User_Registereduser_Appopencount_Year_Quarter
   
    MURAYQ = df[df["Quarter"] == quarter]
    MURAYQ.reset_index(drop = True , inplace = True)

    MURAYQG = MURAYQ.groupby("State")[["Registered_User","App_Open_Count"]].sum() # getting sum values of the count and amount according to state in 2021
    MURAYQG.reset_index(inplace = True) #missligned "State" column rectified by using

    fig_line_2 = px.line(MURAYQG, x = "State", y = ["Registered_User","App_Open_Count"], 
                        title = f"REGISTERED USER & APP OPEN COUNT {MURAYQ['Year'].unique()} - QUARTER:{quarter}",width = 1200, height=800,
                        color_discrete_map= {"Registered_User":"green", "App_Open_Count":"blue"},markers= True 
    )
    st.plotly_chart(fig_line_2)


    return MURAYQ


def t_i_a_c_y_s(df, State):
    #tiacys = Top_Insurance_Amount_Count_Year_Statewise

    TIACYS = df[df["State"] == State]
    TIACYS.reset_index(drop = True , inplace = True)

    col1,col2 = st.columns(2)

    with col1:

        fig_bar_1 = px.bar(TIACYS, x = "Year", y = "Transaction_Count",hover_name= "Pincode",
                                        title= f"TRANSACTION_COUNT - {State.upper()}",
                                        color_discrete_sequence= px.colors.sequential.Magenta_r
        )

        st.plotly_chart(fig_bar_1)
    
    with col2:  

        fig_bar_2 = px.bar(TIACYS, x = "Year", y = "Transaction_Amount",hover_name= "Pincode",
                                        title= f"TRANSACTION_AMOUNT - {State.upper()}",
                                        color_discrete_sequence= px.colors.sequential.Greens_r
        )

        st.plotly_chart(fig_bar_2)

    return TIACYS

def t_i_a_c_y_q_s(df, State):
    #tiacys = Top_Insurance_Amount_Count_Year&Quarter_Statewise
   
    TIACYQS = df[df["State"] == State]
    TIACYQS.reset_index(drop = True , inplace = True)

    col1,col2 = st.columns(2)

    with col1:

        fig_bar_1 = px.bar(TIACYQS, x = "Quarter", y = "Transaction_Count",hover_name = "Pincode",
                                        title= f"TRANSACTION_COUNT {TIACYQS['Year'].unique()} - {State.upper()}",
                                        color_discrete_sequence= px.colors.sequential.Magenta_r
        )

        st.plotly_chart(fig_bar_1)
    
    with col2:

        fig_bar_2 = px.bar(TIACYQS, x = "Quarter", y = "Transaction_Amount",hover_name= "Pincode",
                                        title= f"TRANSACTION_AMOUNT {TIACYQS['Year'].unique()} - {State.upper()}",
                                        color_discrete_sequence= px.colors.sequential.Greens_r
        )

        st.plotly_chart(fig_bar_2)

    return TIACYQS

#Map_User_Registereduser_Appopencount_Yearly

def t_u_r_y(df, year):

    TURY = df[df["Year"] == year]
    TURY.reset_index(drop=True, inplace=True)

    TURYG = pd.DataFrame(TURY.groupby(["State","Quarter"])["Registered_User"].sum())
    TURYG.reset_index(inplace=True)
    
    fig_bar_1 = px.bar(TURYG, x="State", y="Registered_User",
                       color = "Quarter",hover_name= "State",
                        title=f"REGISTERED USER {[year]}",  
                        width = 1200,height=800,
                        color_continuous_scale= px.colors.sequential.Plasma
   )
    
    st.plotly_chart(fig_bar_1)  # Use this to display the chart

    return TURY


def t_u_r_y_s(df, State):
    #t_u_r_y_s = Top_User_Registereduser_Yearly_State
   

    TURYS = df[df["State"] == State]
    TURYS.reset_index(drop = True , inplace = True)


    fig_bar_1 = px.bar(data_frame= TURYS, x = "Quarter", y = "Registered_User",
                                    title= f"QUARTERLY PINCODEWISE REGISTERED USER  - {State.upper()}",
                                    width=1000 , height=800, color = "Registered_User", hover_data="Pincode",
                                    color_continuous_scale= px.colors.sequential.Plasma_r
   )

    st.plotly_chart(fig_bar_1)

    return TURYS


#SQL Connection

def top_chart_transaction_count(table_name):

        mydb = psycopg2.connect(
                host="localhost",
                user="postgres",      
                password="hari",
                database="Phonepe Pulse Data Visualization and Exploration",
                port="5432")

        cursor = mydb.cursor()

        query1 =    f'''SELECT State, SUM(transaction_count) AS transaction_count
                        FROM {table_name} 
                        GROUP BY State 
                        ORDER BY transaction_count DESC
                        LIMIT 10;'''

        cursor.execute(query1)
        table_1 = cursor.fetchall()
        mydb.commit()

        DF_1 = pd.DataFrame(table_1, columns = ("State", "Transaction_Count"))

        col1,col2 = st.columns(2)

        with col1:

            fig_bar_1 = px.bar(data_frame= DF_1, x = "State", y = "Transaction_Count",
                                            title= f"TOP-10",
                                            width=600 , height=650,hover_name="State",
                                            color_discrete_sequence= px.colors.sequential.Magenta_r
            )

            st.plotly_chart(fig_bar_1)


        query2 =    f'''SELECT State, SUM(transaction_count) AS transaction_count
                        FROM {table_name} 
                        GROUP BY State 
                        ORDER BY transaction_count
                        LIMIT 10;'''

        cursor.execute(query2)
        table_2 = cursor.fetchall()
        mydb.commit()

        DF_2 = pd.DataFrame(table_2, columns = ("State", "Transaction_Count"))

        with col2:

            fig_bar_2 = px.bar(data_frame= DF_2, x = "State", y = "Transaction_Count",
                                            title= f"BOTTOM-10",
                                            width=600 , height=720,hover_name="State",
                                            color_discrete_sequence= px.colors.sequential.Magenta_r
            )

            st.plotly_chart(fig_bar_2)



        query3 =    f'''SELECT State, AVG(transaction_count) AS transaction_count
                        FROM {table_name} 
                        GROUP BY State 
                        ORDER BY transaction_count;'''

        cursor.execute(query3)
        table_3 = cursor.fetchall()
        mydb.commit()

        DF_3 = pd.DataFrame(table_3, columns = ("State", "Transaction_Count"))


        fig_bar_3 = px.bar(data_frame= DF_3, y = "State", x = "Transaction_Count", orientation="h",
                                        title= f"AVERAGE", 
                                        width=1000 , height=800,hover_name="State",
                                        color_discrete_sequence= px.colors.sequential.Magenta_r
        )

        st.plotly_chart(fig_bar_3)



#SQL Connection

def top_chart_transaction_amount(table_name):

        mydb = psycopg2.connect(
                host="localhost",
                user="postgres",      
                password="hari",
                database="Phonepe Pulse Data Visualization and Exploration",
                port="5432")

        cursor = mydb.cursor()

        query1 =    f'''SELECT State, SUM(transaction_amount) AS transaction_amount
                        FROM {table_name} 
                        GROUP BY State 
                        ORDER BY transaction_amount DESC
                        LIMIT 10;'''

        cursor.execute(query1)
        table_1 = cursor.fetchall()
        mydb.commit()

        DF_1 = pd.DataFrame(table_1, columns = ("State", "transaction_amount"))

        col1,col2 = st.columns(2)

        with col1:

            fig_bar_1 = px.bar(data_frame= DF_1, x = "State", y = "transaction_amount",
                                            title= f"TOP-10",
                                            width=600 , height=650,hover_name="State", 
                                            color_discrete_sequence= px.colors.sequential.Greens_r
            )

            st.plotly_chart(fig_bar_1)


        query2 =    f'''SELECT State, SUM(transaction_amount) AS transaction_amount
                        FROM {table_name} 
                        GROUP BY State 
                        ORDER BY transaction_amount
                        LIMIT 10;'''

        cursor.execute(query2)
        table_2 = cursor.fetchall()
        mydb.commit()

        DF_2 = pd.DataFrame(table_2, columns = ("State", "transaction_amount"))

        with col2:

            fig_bar_2 = px.bar(data_frame= DF_2, x = "State", y = "transaction_amount",
                                            title= f"BOTTOM-10",
                                            width=600 , height=720,hover_name="State",
                                            color_discrete_sequence= px.colors.sequential.Greens_r
           )

            st.plotly_chart(fig_bar_2)



        query3 =    f'''SELECT State, AVG(transaction_amount) AS transaction_amount
                        FROM {table_name} 
                        GROUP BY State 
                        ORDER BY transaction_amount;'''

        cursor.execute(query3)
        table_3 = cursor.fetchall()
        mydb.commit()

        DF_3 = pd.DataFrame(table_3, columns = ("State", "transaction_amount"))


        fig_bar_3 = px.bar(data_frame= DF_3, y = "State", x = "transaction_amount", orientation="h",
                                        title= f"AVERAGE", 
                                        width=1000 , height=800,hover_name="State",
                                        color_discrete_sequence= px.colors.sequential.Greens_r
        )

        st.plotly_chart(fig_bar_3)



#SQL Connection

def top_chart_registered_user_mu(table_name, state):

        mydb = psycopg2.connect(
                host="localhost",
                user="postgres",      
                password="hari",
                database="Phonepe Pulse Data Visualization and Exploration",
                port="5432")

        cursor = mydb.cursor()

        query1 =    f'''SELECT district_name, SUM(registered_user) AS registered_user
                        FROM {table_name}
                        WHERE state = '{state}'
                        GROUP BY district_name ORDER BY registered_user DESC
                        LIMIT 10;'''

        cursor.execute(query1)
        table_1 = cursor.fetchall()
        mydb.commit()

        DF_1 = pd.DataFrame(table_1, columns = ("District_name", "Registered_User"))

        col1,col2 = st.columns(2)

        with col1:


            fig_bar_1 = px.bar(data_frame= DF_1, x = "District_name", y = "Registered_User",
                                            title= f"TOP-10 REGISTERED USER",
                                            width=600 , height=650,hover_name="District_name",
                                            color_discrete_sequence= px.colors.sequential.Magenta_r
            )

            st.plotly_chart(fig_bar_1)


        query2 =    f'''SELECT district_name, SUM(registered_user) AS registered_user
                        FROM {table_name}
                        WHERE state = '{state}'
                        GROUP BY district_name ORDER BY registered_user 
                        LIMIT 10;'''

        cursor.execute(query2)
        table_2 = cursor.fetchall()
        mydb.commit()

        DF_2 = pd.DataFrame(table_2, columns = ("District_name", "Registered_User"))

        with col2:


            fig_bar_2 = px.bar(data_frame= DF_2, x = "District_name", y = "Registered_User",
                                            title= f"BOTTOM-10 REGISTERED USER",
                                            width=600 , height=650,hover_name="District_name",
                                            color_discrete_sequence= px.colors.sequential.Magenta_r
            )

            st.plotly_chart(fig_bar_2)



        query3 =    f'''SELECT district_name, AVG(registered_user) AS registered_user
                        FROM {table_name}
                        WHERE state = '{state}'
                        GROUP BY district_name ORDER BY registered_user;'''

        cursor.execute(query3)
        table_3 = cursor.fetchall()
        mydb.commit()

        DF_3 = pd.DataFrame(table_3, columns = ("District_name", "Registered_User"))


        fig_bar_3 = px.bar(data_frame= DF_3, y = "District_name", x = "Registered_User", orientation="h",
                                        title= f"AVERAGE REGISTERED USER", 
                                        width=600 , height=650,hover_name="District_name",
                                        color_discrete_sequence= px.colors.sequential.Magenta_r
        )

        st.plotly_chart(fig_bar_3)


#SQL Connection

def top_chart_app_open_count(table_name, state):

        mydb = psycopg2.connect(
                host="localhost",
                user="postgres",      
                password="hari",
                database="Phonepe Pulse Data Visualization and Exploration",
                port="5432")

        cursor = mydb.cursor()

        query1 =    f'''SELECT district_name, SUM(app_open_count) AS app_open_count
                        FROM {table_name}
                        WHERE state = '{state}'
                        GROUP BY district_name ORDER BY app_open_count DESC
                        LIMIT 10;'''

        cursor.execute(query1)
        table_1 = cursor.fetchall()
        mydb.commit()

        DF_1 = pd.DataFrame(table_1, columns = ("District_name", "App_Open_Count"))

        col1,col2 = st.columns(2)

        with col1:


            fig_bar_1 = px.bar(data_frame= DF_1, x = "District_name", y = "App_Open_Count",
                                            title= f"TOP-10 APP OPEN COUNT",
                                            width=600 , height=650,hover_name="District_name",
                                            color_discrete_sequence= px.colors.sequential.Greens_r
           )

            st.plotly_chart(fig_bar_1)


        query2 =    f'''SELECT district_name, SUM(app_open_count) AS app_open_count
                        FROM {table_name}
                        WHERE state = '{state}'
                        GROUP BY district_name ORDER BY app_open_count 
                        LIMIT 10;'''

        cursor.execute(query2)
        table_2 = cursor.fetchall()
        mydb.commit()

        DF_2 = pd.DataFrame(table_2, columns = ("District_name", "App_Open_Count"))

        with col2:


            fig_bar_2 = px.bar(data_frame= DF_2, x = "District_name", y = "App_Open_Count",
                                            title= f"BOTTOM-10 APP OPEN COUNT",
                                            width=600 , height=650,hover_name="District_name",
                                            color_discrete_sequence= px.colors.sequential.Greens_r
            )

            st.plotly_chart(fig_bar_2)



        query3 =    f'''SELECT district_name, AVG(app_open_count) AS app_open_count
                        FROM {table_name}
                        WHERE state = '{state}'
                        GROUP BY district_name ORDER BY app_open_count;'''

        cursor.execute(query3)
        table_3 = cursor.fetchall()
        mydb.commit()

        DF_3 = pd.DataFrame(table_3, columns = ("District_name", "App_Open_Count"))


        fig_bar_3 = px.bar(data_frame= DF_3, y = "District_name", x = "App_Open_Count", orientation="h",
                                        title= f"AVERAGE APP OPEN COUNT", 
                                        width=600 , height=650,hover_name="District_name",
                                        color_discrete_sequence= px.colors.sequential.Greens_r
        )

        st.plotly_chart(fig_bar_3)


#SQL Connection

def top_chart_registered_user_tu(table_name):

        mydb = psycopg2.connect(
                host="localhost",
                user="postgres",      
                password="hari",
                database="Phonepe Pulse Data Visualization and Exploration",
                port="5432")

        cursor = mydb.cursor()

        query1 =    f'''SELECT state, SUM(registered_user) AS registered_user
                        from {table_name}
                        GROUP BY state
                        ORDER BY registered_user DESC
                        LIMIT 10;'''

        cursor.execute(query1)
        table_1 = cursor.fetchall()
        mydb.commit()

        DF_1 = pd.DataFrame(table_1, columns = ("State", "Registered_User"))

        col1,col2 = st.columns(2)

        with col1:


            fig_bar_1 = px.bar(data_frame= DF_1, x = "State", y = "Registered_User",
                                            title= f"TOP-10 REGISTERED USER",
                                            width=600 , height=650,hover_name="State",
                                            color_discrete_sequence= px.colors.sequential.Magenta_r
            )

            st.plotly_chart(fig_bar_1)


        query2 =    f'''SELECT state, SUM(registered_user) AS registered_user
                        from {table_name}
                        GROUP BY state
                        ORDER BY registered_user DESC
                        LIMIT 10;'''

        cursor.execute(query2)
        table_2 = cursor.fetchall()
        mydb.commit()

        DF_2 = pd.DataFrame(table_2, columns = ("State", "Registered_User"))

        with col2:


            fig_bar_2 = px.bar(data_frame= DF_2, x = "State", y = "Registered_User",
                                            title= f"BOTTOM-10 REGISTERED USER",
                                            width=600 , height=650,hover_name="State",
                                            color_discrete_sequence= px.colors.sequential.Magenta_r
            )

            st.plotly_chart(fig_bar_2)



        query3 =    f'''SELECT state, AVG(registered_user) AS registered_user
                        from {table_name}
                        GROUP BY state
                        ORDER BY registered_user;'''

        cursor.execute(query3)
        table_3 = cursor.fetchall()
        mydb.commit()

        DF_3 = pd.DataFrame(table_3, columns = ("State", "Registered_User"))


        fig_bar_3 = px.bar(data_frame= DF_3, y = "State", x = "Registered_User", orientation="h",
                                        title= f"AVERAGE REGISTERED USER", 
                                        width=600 , height=650,hover_name="State",
                                        color_discrete_sequence= px.colors.sequential.Magenta_r
        )

        st.plotly_chart(fig_bar_3)



def top_chart_transaction_type_at(table_name, state):

            mydb = psycopg2.connect(
            host="localhost",
            user="postgres",      
            password="hari",
            database="Phonepe Pulse Data Visualization and Exploration",
            port="5432")

            cursor = mydb.cursor()

            query1 =    f'''SELECT transaction_type, SUM(transaction_count) AS transaction_count
                            FROM {table_name}
                            WHERE state = '{state}'
                            GROUP BY transaction_type ORDER BY transaction_count DESC
                            LIMIT 10;'''


            cursor.execute(query1)
            table_1 = cursor.fetchall()
            mydb.commit()

            DF_1 = pd.DataFrame(table_1, columns = ("transaction_type", "transaction_count"))

            col1,col2 = st.columns(2)

            with col1:


                fig_bar_1 = px.bar(data_frame= DF_1, x = "transaction_type", y = "transaction_count",
                                                title= f"TOP-10",
                                                width=600 , height=650,hover_name="transaction_type",
                                                color_discrete_sequence= px.colors.sequential.Greens_r
                )

                st.plotly_chart(fig_bar_1)


            query2 =    f'''SELECT transaction_type, SUM(transaction_amount) AS transaction_amount
                            FROM {table_name}
                            WHERE state = '{state}'
                            GROUP BY transaction_type ORDER BY transaction_amount 
                            LIMIT 10;'''

            cursor.execute(query2)
            table_2 = cursor.fetchall()
            mydb.commit()

            DF_2 = pd.DataFrame(table_2, columns = ("transaction_type", "transaction_amount"))

            with col2:


                fig_bar_2 = px.bar(data_frame= DF_2, x = "transaction_type", y = "transaction_amount",
                                                title= f"BOTTOM-10",
                                                width=600 , height=650,hover_name="transaction_type",
                                                color_discrete_sequence= px.colors.sequential.Magenta_r
                )

                st.plotly_chart(fig_bar_2)



            query3 =    f'''SELECT transaction_type, SUM(transaction_amount) / NULLIF(SUM(transaction_count), 0) AS average_transaction_value
                            FROM {table_name}
                            WHERE state = '{state}'
                            GROUP BY transaction_type ORDER BY average_transaction_value;'''

            cursor.execute(query3)
            table_3 = cursor.fetchall()
            mydb.commit()

            DF_3 = pd.DataFrame(table_3, columns = ("transaction_type", "average_transaction_value"))


            fig_bar_3 = px.bar(data_frame= DF_3, y = "transaction_type", x = "average_transaction_value", orientation="h",
                                            title= f"AVERAGE TRANSACTION VALUE", 
                                            width=600 , height=650,hover_name="transaction_type",
                                            color_discrete_sequence= px.colors.sequential.Plasma
            )

            st.plotly_chart(fig_bar_3)



def top_chart_transaction_type_auc(table_name, state):

            mydb = psycopg2.connect(
            host="localhost",
            user="postgres",      
            password="hari",
            database="Phonepe Pulse Data Visualization and Exploration",
            port="5432")

            cursor = mydb.cursor()

            query1 =    f'''SELECT brand, SUM(transaction_count) AS transaction_count
                            FROM "{table_name}"
                            GROUP BY brand ORDER BY transaction_count DESC
                            LIMIT 10;'''


            cursor.execute(query1)
            table_1 = cursor.fetchall()
            mydb.commit()

            DF_1 = pd.DataFrame(table_1, columns = ( "brand", "transaction_count"))

            


            fig_bar_1 = px.bar(data_frame= DF_1, x = "brand", y = "transaction_count", 
                                            title= f"TOP-10",
                                            width=1000 , height=650,hover_name="brand",
                                            color_discrete_sequence= px.colors.sequential.Greens_r
            )

            st.plotly_chart(fig_bar_1)


            query2 =    f'''SELECT brand, SUM(transaction_count) AS transaction_count
                            FROM "{table_name}"
                            GROUP BY brand ORDER BY transaction_count 
                            LIMIT 10;;'''

            cursor.execute(query2)
            table_2 = cursor.fetchall()
            mydb.commit()

            DF_2 = pd.DataFrame(table_2, columns = ("brand", "transaction_count"))

           


            fig_bar_2 = px.bar(data_frame= DF_2, x = "brand", y = "transaction_count",
                                            title= f"BOTTOM-10",
                                            width=1000 , height=650,hover_name="brand",
                                            color_discrete_sequence= px.colors.sequential.Magenta_r
           )

            st.plotly_chart(fig_bar_2)


#SQL Connection

def top_chart_transaction_count_map_insurance_districtwise (table_name):

        mydb = psycopg2.connect(
                host="localhost",
                user="postgres",      
                password="hari",
                database="Phonepe Pulse Data Visualization and Exploration",
                port="5432")

        cursor = mydb.cursor()

        query1 =    f'''SELECT district_name, SUM(transaction_count) AS transaction_count 
                        FROM {table_name}
                        GROUP BY district_name ORDER BY transaction_count DESC
                        LIMIT 20;'''

        cursor.execute(query1)
        table_1 = cursor.fetchall()
        mydb.commit()

        DF_1 = pd.DataFrame(table_1, columns = ("district_name", "transaction_count"))


        fig_area_1 = px.area(data_frame= DF_1, x = "district_name", y = "transaction_count",
                                        title= f"TOP 20",labels= {'district_name':"District_Name","transaction_count": "Transaction_Count"},
                                        width=1000 , height=650,
                                        color_discrete_sequence=px.colors.sequential.Greens_r
        )

        st.plotly_chart(fig_area_1)


        query2 =    f'''SELECT district_name, SUM(transaction_count) AS transaction_count 
                        FROM {table_name}
                        GROUP BY district_name ORDER BY transaction_count 
                        LIMIT 20;'''

        cursor.execute(query2)
        table_2 = cursor.fetchall()
        mydb.commit()

        DF_2 = pd.DataFrame(table_2, columns = ("district_name", "transaction_count"))


        fig_area_2 = px.area(data_frame= DF_2, x = "district_name", y = "transaction_count",
                                        title= f"BOTTOM 20",labels= {'district_name':"District_Name","transaction_count": "Transaction_Count"},
                                        width=1000 , height=650,
                                        color_discrete_sequence=px.colors.sequential.Oranges_r
        )

        st.plotly_chart(fig_area_2)



        query3 =    f'''SELECT year, AVG(transaction_count) AS transaction_count 
                        FROM {table_name}
                        GROUP BY year ORDER BY
                        transaction_count;'''

        cursor.execute(query3)
        table_3 = cursor.fetchall()
        mydb.commit()

        DF_3 = pd.DataFrame(table_3, columns = ("year", "transaction_count"))


        fig_funnel_3 = px.funnel_area(data_frame= DF_3, names="year", values="transaction_count",
                                        title= f"AVERAGE",labels= {'year':"Year","transaction_count": "Transaction_Count"},
                                        width=1000 , height=650
                                        )

        st.plotly_chart(fig_funnel_3)


#SQL Connection

def top_chart_transaction_amount_map_insurance_districtwise (table_name):

        mydb = psycopg2.connect(
                host="localhost",
                user="postgres",      
                password="hari",
                database="Phonepe Pulse Data Visualization and Exploration",
                port="5432")

        cursor = mydb.cursor()

        query1 =    f'''SELECT district_name, SUM(transaction_amount) AS transaction_amount 
                        FROM {table_name}
                        GROUP BY district_name ORDER BY transaction_amount DESC
                        LIMIT 20;'''

        cursor.execute(query1)
        table_1 = cursor.fetchall()
        mydb.commit()

        DF_1 = pd.DataFrame(table_1, columns = ("district_name", "transaction_amount"))


        fig_area_1 = px.area(data_frame= DF_1, x = "district_name", y = "transaction_amount",
                                        title= f"TOP 20",labels= {'district_name':"District_Name","transaction_amount": "Transaction_Amount"},
                                        width=1000 , height=650,
                                        color_discrete_sequence=px.colors.sequential.Greens_r
        )

        st.plotly_chart(fig_area_1)


        query2 =    f'''SELECT district_name, SUM(transaction_amount) AS transaction_amount 
                        FROM {table_name}
                        GROUP BY district_name ORDER BY transaction_amount 
                        LIMIT 20;'''

        cursor.execute(query2)
        table_2 = cursor.fetchall()
        mydb.commit()

        DF_2 = pd.DataFrame(table_2, columns = ("district_name", "transaction_amount"))


        fig_area_2 = px.area(data_frame= DF_2, x = "district_name", y = "transaction_amount",
                                        title= f"BOTTOM 20",labels= {'district_name':"District_Name","transaction_amount": "Transaction_Amount"},
                                        width=1000 , height=650,
                                        color_discrete_sequence=px.colors.sequential.Oranges_r
        )

        st.plotly_chart(fig_area_2)



        query3 =    f'''SELECT year, AVG(transaction_amount) AS transaction_amount 
                        FROM {table_name}
                        GROUP BY year ORDER BY
                        transaction_amount;'''

        cursor.execute(query3)
        table_3 = cursor.fetchall()
        mydb.commit()

        DF_3 = pd.DataFrame(table_3, columns = ("year", "transaction_amount"))


        fig_funnel_3 = px.funnel_area(data_frame= DF_3, names="year", values="transaction_amount",
                                        title= f"AVERAGE",labels= {'year':"Year","transaction_amount": "Transaction_Amount"},
                                        width=1000 , height=650
        )

        st.plotly_chart(fig_funnel_3)



#Streamlit Part

st.set_page_config(layout = "wide")
st.image(r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\PhonePe_Logo.svg.png", width=300)
st.title("PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION")


with st.sidebar:
    st.logo("C:/Users/dell/Downloads/pngwing.com.png")

    select = option_menu(
                menu_title="Menu",options=["HOME", "DATA EXPLORATION", "TOP CHARTS", "ABOUT", "CONTACT"],
                icons= ["house", "bar-chart", "list-task", "info-circle", "envelope"],
                menu_icon="cast",orientation="vertical",  
                styles={"container": {"padding": "3px", "background-color": "#f5f2fa"},
                        "icon": {"color": "orange", "font-size": "20px"},
                        "nav-link": {
                        "font-size": "18px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#eee",},
                        "nav-link-selected": {"background-color": "#6231b5"}} 
    )
    

if select == "HOME":


    IMAGES = [
        r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\1.png",
        r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\2.png",
        r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\3.png",
    ]


    def encode_image_to_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    def slideshow_swipeable(images, auto_slide=True, interval=2):
        # Generate a session state key based on images.
        key = f"slideshow_swipeable_{str(images).encode().hex()}"

        # Initialize the default slideshow index.
        if key not in st.session_state:
            st.session_state[key] = 0

        # Update the index if auto_slide is enabled.
        if auto_slide:
            time.sleep(interval)  # Delay for the specified interval
            st.session_state[key] = (st.session_state[key] + 1) % len(images)  # Loop back to start

        # Get the current slideshow index.
        index = st.session_state[key]

        # Create a new elements frame.
        with elements(f"frame_{key}"):
            # Use mui.Stack to vertically display the slideshow and the pagination centered.
            with mui.Stack(spacing=2, alignItems="center"):
                # Create a swipeable view that updates st.session_state[key] thanks to sync().
                with mui.SwipeableViews(index=index, resistance=True, onChangeIndex=sync(key)):
                    for image in images:
                        encoded_image = encode_image_to_base64(image)
                        img_src = f"data:image/jpg;base64,{encoded_image}"
                        html.img(src=img_src, css={"width": "100%"})

                # Create a handler for mui.Pagination.
                def handle_change(event, value):
                    st.session_state[key] = value - 1

                # Display the pagination.
                mui.Pagination(page=index + 1, count=len(images), color="primary", onChange=handle_change)

    if __name__ == '__main__':
        slideshow_swipeable(IMAGES)

    
    st.subheader("🚀 India's Leading digital payments and financial services app 🚀")
    st.markdown("""**PhonePe** is Founded in 2015, It has rapidly grown into one of India's most popular 
                digital payment platforms. Offering a wide range of financial services, PhonePe simplifies 
                daily transactions and empowers users to manage their money with ease.""")
    
    st.markdown("""_______________________________________________________________________________________________________________""")
    
    st.markdown("### 🔹 **KEY SERVICES** 🔹")
        
        

         
    col1,col2 = st.columns(2)

    with col1:
        st.markdown("""
                    ***💸 Mobile Payments***: Send and receive money instantly to friends, family, and businesses""")
        st.image(r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\phonepe.gif",width=500)

    with col2:
        st.markdown("""
                    ***💡 Bill Payments***: Pay utility bills, recharge mobile and DTH connections, and more""")
        st.image(r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\unnamed.webp", width=400)

    st.markdown("""_______________________________________________________________________________________________________________""")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
                    ***📲 Recharge & Postpaid***: Top up your mobile and DTH plans, and pay your postpaid bills""")
        st.image(r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\hq720.jpg")
                    
    with col4:
        st.markdown("""
                    ***✈️ Travel Bookings***: Book flights, hotels, and bus tickets directly from the app""") 
        st.image(r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\309143442_5648848425179829_1623875021734241893_n.jpg", width=400)    

    st.markdown("""_______________________________________________________________________________________________________________""")

    col5,col6 = st.columns(2)

    with col5:
        st.markdown("""
                    ***🛡️ Insurance***: Purchase various types of insurance, including life, health, and vehicle insurance""")
        st.image(r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\136452578_3783332755064748_7558774532561030684_n.png",width=400)

    with col6:
        st.markdown("""
                    ***📈 Investments***: Explore investment options like mutual funds and gold""")
        st.image(r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\step1-desktop.png",width=400)
    
    st.markdown("""_______________________________________________________________________________________________________________""")

        
        
                
    st.markdown("""
                ***🔗 UPI Payments**: Make instant bank transfers using the Unified Payments Interface (UPI)""")
    
    Video_URL = "https://www.youtube.com/watch?v=JTt405gG6P0&t=8s"
    st.video(Video_URL)


    col1,col2 = st.columns(2)

    with col1:
        st.header(":violet[18152+ Crore]")
        st.subheader(":violet[Transactions]")
        st.write(":violet[**Top trends across india's digital payment industry**]")

    with col2:
        st.video(r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\pulse-video.mp4")


    st.markdown("### 📲 **Get Started Today!**")

    if st.button("DOWNLOAD THE APP NOW"):
        st.write("[Go to Download Page](https://play.google.com/store/apps/details?id=com.phonepe.app&pcampaignid=web_share)")
                            
                            
    
elif select == "DATA EXPLORATION":


    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis" , "Top Analysis"])

    with tab1:
        method1 = st.radio("Select The Method", ["Aggregated Insurance", "Aggregated Transaction", "Aggregated User" ])

        if method1 == "Aggregated Insurance":

            col1,col2 = st.columns(2)
            with col1:
            
                Year = st.slider("Select The Year", 
                                Aggregated_Insurance_DF["Year"].min(),
                                Aggregated_Insurance_DF["Year"].max(),
                                Aggregated_Insurance_DF["Year"].min(),
                                key = "AIY_Slider")
            
            aiacy = a_i_a_c_y(Aggregated_Insurance_DF, Year)

            col1,col2 = st.columns(2)
            with col1:
                
                Quarter = st.slider("Select The Quarter", 
                                aiacy["Quarter"].min(),
                                aiacy["Quarter"].max(),
                                aiacy["Quarter"].min(),
                                key = "AIQ_Slider")
                
            aiacyq = a_i_a_c_y_q(aiacy,Quarter)
            

        elif method1 == "Aggregated Transaction":

            col1, col2 = st.columns(2)
            with col1:

                Year = st.slider("Select The Year", 
                                Aggregated_Transaction_DF["Year"].min(),
                                Aggregated_Transaction_DF["Year"].max(),
                                Aggregated_Transaction_DF["Year"].min(),
                                key = "ATY_Slider")

           
            atacy = a_i_a_c_y(Aggregated_Transaction_DF, Year)


            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Yearly (Transaction Type)", atacy["State"].unique())
            atacts = a_t_a_c_t_s(atacy , State)

      
            col1, col2 = st.columns(2)
            with col1:

                Quarter = st.slider("Select The Quarter", 
                                    atacy["Quarter"].min(),
                                    atacy["Quarter"].max(),
                                    atacy["Quarter"].min(),
                                    key = "ATQ_Slider")

            # Calculate the result based on the selected quarter
            atacyq = a_i_a_c_y_q(atacy, Quarter)

            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Quarterly (Transaction Type)", atacyq["State"].unique())
            atactsq = a_t_a_c_t_s(atacyq , State)


        elif method1 == "Aggregated User":
            col1,col2 = st.columns(2)
            with col1:
            
                Year = st.slider("Select The Year", 
                                Aggregated_User_DF["Year"].min(),
                                Aggregated_User_DF["Year"].max(),
                                Aggregated_User_DF["Year"].min(),
                                key = "AUY_Slider")
                
            aubay = a_u_b_a_y(Aggregated_User_DF,Year)
            #aubay = #Aggregated_User_Brand_Amount_Yearwise


            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State [Yearly]", aubay["State"].unique())
            aubays = a_u_b_a_y_s(aubay , State)


            col1,col2 = st.columns(2)
            with col1:
            
                Quarter = st.slider("Select The Quarter", 
                                aubay["Quarter"].min(),
                                aubay["Quarter"].max(),
                                aubay["Quarter"].min(),
                                key = "AUQ_Slider")
                
            aubayq = a_u_b_a_y_q (aubay,Quarter)
            #a_u_b_a_y_q = Aggregated_User_Brand_Amount_Year_Quarterwise


            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State [Quarterly]", aubayq["State"].unique())
            aubayqs = a_u_b_a_y_s(aubayq , State)
            #a_u_b_a_y_q_s = Aggregated_User_Brand_Amount_Year_Quarterwise_Statewise


    with tab2:
        method2 = st.radio("Select The Method", ["Map Insurance", "Map Transaction", "Map User"])

        if method2 == "Map Insurance":

            col1, col2 = st.columns(2)
            with col1:

                Year = st.slider("Select The Year", 
                                Map_Insurance_DF["Year"].min(),
                                Map_Insurance_DF["Year"].max(),
                                Map_Insurance_DF["Year"].min(),
                                key = "MIY_Slider")


            miacy = a_i_a_c_y(Map_Insurance_DF, Year)

            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Yearly [Districtwise Transactions]", miacy["State"].unique())
            miacys = m_i_a_c_y_s(miacy , State)


            col1, col2 = st.columns(2)
            with col1:

                Quarter = st.slider("Select The Quarter", 
                                miacy["Quarter"].min(),
                                miacy["Quarter"].max(),
                                miacy["Quarter"].min(),
                                key = "MIQ_Slider")

            miacyq = a_i_a_c_y_q(miacy,Quarter)

            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Quarterly [Districtwise Transactions]", miacyq["State"].unique())
            miacyqs = m_i_a_c_y_s (miacyq , State)


        elif method2 == "Map Transaction":

            col1, col2 = st.columns(2)
            with col1:

                Year = st.slider("Select The Year", 
                                Map_Transaction_DF["Year"].min(),
                                Map_Transaction_DF["Year"].max(),
                                Map_Transaction_DF["Year"].min(),
                                key = "MTY_Slider")
                
            mtacy = a_i_a_c_y(Map_Transaction_DF, Year)


            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Yearly [Districtwise Transactions]", mtacy["State"].unique())
            mtacys = m_i_a_c_y_s(mtacy , State)

            col1, col2 = st.columns(2)
            with col1:

                Quarter = st.slider("Select The Quarter", 
                                mtacy["Quarter"].min(),
                                mtacy["Quarter"].max(),
                                mtacy["Quarter"].min(),
                                key = "MTQ_Slider")

            mtacyq = a_i_a_c_y_q(mtacy,Quarter)


            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Quarterly [Districtwise Transactions]", mtacyq["State"].unique())
            mtacyqs = m_i_a_c_y_s (mtacyq , State)


        elif method2 == "Map User":

            col1,col2 = st.columns(2)
            with col1:
            
                Year = st.slider("Select The Year", 
                                Map_User_DF["Year"].min(),
                                Map_User_DF["Year"].max(),
                                Map_User_DF["Year"].min(),
                                key = "MUY_Slider")
            
            muray = m_u_r_a_y(Map_User_DF, Year)


            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Yearly [Districtwise Registered & Open Count]", muray["State"].unique())
            murays = m_u_r_a_y_s(muray , State)


            col1,col2 = st.columns(2)
            with col1:
            
                Quarter = st.slider("Select The Quarter", 
                                muray["Quarter"].min(),
                                muray["Quarter"].max(),
                                muray["Quarter"].min(),
                                key = "MUQ_Slider")
                
            murayq = m_u_r_a_y_q(muray,Quarter)
                
           
            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Quarterly [Districtwise Registered & Open Count]", murayq["State"].unique())
            murayqs = m_u_r_a_y_s(murayq , State)

    with tab3:
        method3 = st.radio("Select The Method", ["Top Insurance", "Top Transaction", "Top User"])

        if method3 == "Top Insurance":
            

            col1,col2 = st.columns(2)
            with col1:
        
                Year = st.slider("Select The Year", 
                                Top_Insurance_DF["Year"].min(),
                                Top_Insurance_DF["Year"].max(),
                                Top_Insurance_DF["Year"].min(),
                                key = "TIY_Slider")
            tiacy = a_i_a_c_y(Top_Insurance_DF, Year)


            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Yearly [Pincodewise Transactions]", Top_Insurance_DF["State"].unique())
            tiacys = t_i_a_c_y_s(Top_Insurance_DF , State)



            col1,col2 = st.columns(2)
            with col1:
            
                Quarter = st.slider("Select The Quarter", 
                                tiacy["Quarter"].min(),
                                tiacy["Quarter"].max(),
                                tiacy["Quarter"].min(),
                                key = "TIQ_Slider")
                
            tiacyq = a_i_a_c_y_q(tiacy,Quarter)


            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Quarterly [Pincodewise Transactions]", tiacy["State"].unique())
            tiacyqs = t_i_a_c_y_q_s(tiacy , State)



        elif method3 == "Top Transaction":

            
            col1,col2 = st.columns(2)
            with col1:
        
                Year = st.slider("Select The Year", 
                                Top_Transaction_DF["Year"].min(),
                                Top_Transaction_DF["Year"].max(),
                                Top_Transaction_DF["Year"].min(),
                                key = "TTY_Slider")
            ttacy = a_i_a_c_y(Top_Transaction_DF, Year)


            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Yearly [Pincodewise Transactions]", Top_Transaction_DF["State"].unique())
            ttacys = t_i_a_c_y_s(Top_Transaction_DF , State)



            col1,col2 = st.columns(2)
            with col1:
            
                Quarter = st.slider("Select The Quarter", 
                                ttacy["Quarter"].min(),
                                ttacy["Quarter"].max(),
                                ttacy["Quarter"].min(),
                                key = "TTQ_Slider")
                
            ttacyq = a_i_a_c_y_q(ttacy,Quarter)


            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Quarterly [Pincodewise Transactions]", ttacy["State"].unique())
            ttacyqs = t_i_a_c_y_q_s(ttacy , State)


        elif method3 == "Top User":

            col1,col2 = st.columns(2)
            with col1:
        
                Year = st.slider("Select The Year", 
                                Top_User_DF["Year"].min(),
                                Top_User_DF["Year"].max(),
                                Top_User_DF["Year"].min(),
                                key = "TUY_Slider")
            tury = t_u_r_y(Top_User_DF, Year)


            col1,col2 = st.columns(2)
            with col1:

                State = st.selectbox("Select The State - Quarterly [Pincodewise Transactions]", tury["State"].unique())
            turys = t_u_r_y_s(tury, State)


elif select == "TOP CHARTS":
    question = st.selectbox("Select The Question", ["1. Transaction Count and Amount of Aggregated Insurance",

                                                    "2. Transaction Count and Amount of Map Insurance",

                                                    "3. Transaction Count and Amount of Top Insurance",

                                                    "4. Transaction Count and Amount of Aggregated Transaction",

                                                    "5. Transaction Count and Amount of Map Transaction",

                                                    "6. Transaction Count and Amount of Top Transaction",

                                                    "7. Transaction Count of Aggregated User",

                                                    "8. Registered users of Map User",

                                                    "9. App open count of Map User",

                                                    "10. Registered users of Top User",
                                                    
                                                    "11. Transaction type performance of aggregated transation",
                                                    
                                                    "12. Brand performance yearwise of aggregated user",

                                                    "13. Top and Bottom Districtwise Transaction Count of map insurance",
                                                    
                                                    "14. Top and Bottom Districtwise Transaction Count of map transaction",
                                                    
                                                    "15. Top and Bottom Districtwise Transaction Amount of map insurance",
                                                    
                                                    "16. Top and Bottom Districtwise Transaction Amount of map transaction"])

           
    if question == "1. Transaction Count and Amount of Aggregated Insurance":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")


    elif question == "2. Transaction Count and Amount of Map Insurance":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")


    elif question == "3. Transaction Count and Amount of Top Insurance":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")


    elif question == "4. Transaction Count and Amount of Aggregated Transaction":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")


    elif question == "5. Transaction Count and Amount of Map Transaction":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")


    elif question == "6. Transaction Count and Amount of Top Transaction":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")


    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

        
    elif question == "8. Registered users of Map User":

        state = st.selectbox("Select The State", Map_User_DF["State"].unique()) 
        st.subheader("REGISTERED USER")
        top_chart_registered_user_mu("map_user", state)


    elif question == "9. App open count of Map User":

            state = st.selectbox("Select The State", Map_User_DF["State"].unique()) 
            st.subheader("APP OPEN COUNT")
            top_chart_app_open_count("map_user", state)


    elif question == "10. Registered users of Top User":

            st.subheader("REGISTERED USER")
            top_chart_registered_user_tu("top_user")


    elif question == "11. Transaction type performance of aggregated transation":

        state = st.selectbox("Select The State", Aggregated_Transaction_DF["State"].unique()) 
        st.subheader("AVERAGE TRANSACTION VALUE")
        top_chart_transaction_type_at("aggregated_transaction", state)


    elif question == "12. Brand performance yearwise of aggregated user":

        state = st.selectbox("Select The State", Aggregated_User_DF["State"].unique()) 
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_type_auc("aggregated_user", state)

    elif question == "13. Top and Bottom Districtwise Transaction Count of map insurance":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count_map_insurance_districtwise("map_insurance")

    elif question == "14. Top and Bottom Districtwise Transaction Count of map transaction":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count_map_insurance_districtwise("map_transaction")


    elif question == "15. Top and Bottom Districtwise Transaction Amount of map insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount_map_insurance_districtwise("map_insurance")


    elif question == "16. Top and Bottom Districtwise Transaction Amount of map transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount_map_insurance_districtwise("map_transaction")





elif select == "ABOUT":
    
    Video_URL = "https://www.youtube.com/watch?v=Yy03rjSUIB8&t=1s"
    st.video(Video_URL)
    

    st.markdown("""The **Indian digital payments** story has truly captured the world's imagination. From the largest towns to the remotest villages, 
                    there is a payments revolution being driven by the penetration of mobile phones and data.
                    When PhonePe started 5 years back, we were constantly looking for definitive data sources on digital payments in India.""") 
                    
                
                
    st.markdown( """Some of the questions we were seeking answers to were - How are consumers truly using digital payments? What are the top cases? 
                    Are kiranas across Tier 2 and 3 getting a facelift with the penetration of **QR codes?**""")
                
    st.markdown("""
                    This year as we became India's largest digital payments platform with **46% UPI market share**, 
                    we decided to demystify the what, why and how of digital payments in India.""")   
    st.markdown("""              
                    This year, as we crossed **2000 Cr.** transactions and **30 Crore registered users**, 
                    we thought as India's largest digital payments platform with **46% UPI market share**, 
                    we have a ring-side view of how India sends, spends, manages and grows its money. 
                    So it was time to demystify and share the what, why and how of digital payments in India.
                    PhonePe Pulse is your window to the world of how India transacts with interesting trends, 
                    deep insights and in-depth analysis based on our data put together by the **PhonePe** team.""")
    
    Video_URL = "https://www.youtube.com/watch?v=c_1H6vivsiA"
    st.video(Video_URL)

    st.markdown("""_______________________________________________________________________________________________________________""")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Sameer Nigam (CEO)")

    with col2:

        st.markdown("""**Sameer Nigam** founded PhonePe in 2015 and serves as its **Chief Executive Officer**. Before PhonePe, 
                    he served as the SVP Engineering and VP Marketing at **Flipkart**. 
                    His Flipkart journey started in 2011 when the company acquired his earlier startup - **Mime360**, 
                    a digital media distribution platform. Sameer has also served as the Director of Product Management at **Shopzilla Inc**, 
                    where he built the company's proprietary shopping search engine. **In 2009**, 
                    he won the coveted **Wharton Venture Award**, bestowed by the prestigious **Wharton Business School**. 
                    He holds an **MBA** from the Wharton Business School (University of Pennsylvania), USA, and 
                    a **Master’s** degree in **Computer Science** from the University of Arizona, Tucson-USA""")

    with col3:
        st.image(r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\1712076427975.jpg", width=260)


    col1, col2,col3 = st.columns(3)

    with col1:
        st.header("Vision & Mission")

    with col2:
        st.markdown("""To build a large, scalable & open transaction **ecosystem** 
                    that creates the maximum positive impact for all **stakeholders**.""")

    with col3:
        st.markdown("""To offer every **Indian** equal opportunity to accelerate their progress by 
                    unlocking the **flow of money** and **access to services**.""")
        
    st.markdown("""_______________________________________________________________________________________________________________""")
    


    
    col1, col2,col3 = st.columns(3)
    with col1:
        st.header("Ethics")    

    with col2:

        st.markdown("""The PhonePe Group of Companies is committed to complying with the letter and spirit of regional, 
                    national and international laws and regulations and to conduct ourselves ethically with humility, honesty and integrity. 
                    PhonePe’s objective is to maintain the outstanding reputation for trustworthiness we have achieved over the years.
                    Regardless of where each of us works, this Code of Conduct is the guide to exemplifying integrity as a PhonePe employee. 
                    It’s a daily resource for making honest, 
                    fair and objective decisions while operating in compliance with all laws and our policies.""")
        
    with col3:
        st.markdown("""Through your ethical behavior and willingness to speak up for the highest standards, we earn and keep the trust of our customers, 
                    each other and our local communities. PhonePe will be the catalyst for building the next generation of digital payment infrastructure,
                    but only if accomplished through our everyday integrity.
                    Thank you for your commitment to our **Code of Conduct**. 
                    It means more than making ethical decisions; 
                    it demonstrates you care about PhonePe, our reputation and our customers.""")
        
    st.markdown("""_______________________________________________________________________________________________________________""")
        
        
        
    col1,col2,col3 = st.columns(3)

    with col1:
        st.subheader("Customer Support")
        st.markdown("""To get instant help, tap  on your PhonePe app home screen & select the relevant topic""")
        st.write(":violet[**📞 080-68727374/022-68727374**]")

    with col2:
        st.subheader("Grievances")
        st.markdown("""Get in touch with us to escalate any existing complaints, and we will ensure a quick resolution.""")

    with col3:
        st.subheader("Ombudsman")
        st.markdown("""You can direct your complaints to our regulating authority by sending them a message.""")

    st.markdown("""_______________________________________________________________________________________________________________""")

    

    col1,col2 = st.columns(2)

    with col1:

        st.header("Registered Address")
        st.subheader("PhonePe Private Limited")
        st.write("Office-2, Floor 5, Wing A, Block A,")
        st.write("Salarpuria Softzone, Bellandur Village,")
        st.write("Varthur Hobli, Outer Ring Road, Bangalore South,")
        st.write("Bangalore, Karnataka, India, 560103")
        st.write("CIN: U67190KA2012PTC176031")

        if st.button("VIEW IN MAPS"):
            st.write("[Click Here](https://www.google.com/maps/place/Salarpuria+Softzone/@12.924253,77.670086,16z/data=!4m6!3m5!1s0x3bae13760d58dd77:0x5d1703aa07d3ea8b!8m2!3d12.9242528!4d77.6700857!16s%2Fg%2F11cn0xsvfz?hl=en&entry=ttu&g_ep=EgoyMDI0MTAwOS4wIKXMDSoASAFQAw%3D%3D)")

    with col2:

        data = {
                'latitude': [12.92491],
                'longitude': [77.67019] 
        }

        df = pd.DataFrame(data)
    
        st.map(df)
            


        
    
    

elif select == "CONTACT":

    st.header('PROJECT OVERVIEW')
    st.markdown("""This project extracts data from a GitHub repository in JSON format, 
                processes it with Python, and visualizes the results through a Streamlit interface. 
                Below are the key steps involved:""")
    st.subheader("**Steps**")
    st.markdown("""
                1. **Data Extraction**
                    - Cloned the GitHub repository containing the data in JSON format.

                2. **Python Package Installation**
                    - Installed necessary packages: `json`, `pandas`, `streamlit`, and others.

                3. **Data Frame Creation**
                    - Loaded the JSON data and created multiple data frames from the specified file location using pandas.

                4. **Streamlit Interface**
                    - Developed a user interface in Streamlit.
                    - Used the Plotly package to create interactive charts for data visualization.
                
                5. **SQL Integration**
                    - Integrated PostgreSQL to query the data directly and convert query results into data frames.
                
                6. **Chart Visualization**
                    - Generated various charts based on transaction data using pandas and plotly""")
    
    st.markdown("""______________________________________________________________________________________________""")
    
    st.subheader("Technologies Used")
    st.markdown("""
                **Python**: Data processing and application logic.

                **Pandas**: Data frame manipulation.

                **Streamlit**: Web application framework for creating interactive dashboards.

                **Plotly**: Visualization library for creating charts.
                
                **PostgreSQL**: Database used for SQL queries and data storage""")
    
    st.markdown("""______________________________________________________________________________________________""")
    
    

    col1,col2,col3 = st.columns(3)

    with col1:
        st.subheader("Contact")
        st.write("**rkarikalan003@gmail.com**")

    with col2:
        st.subheader("KARIKALAN.R")
        st.write("**B.E**")
    
    with col3:
        st.image(r"C:\Users\dell\Desktop\GUVI Projects\Phonepe Project\Images\phohto.jpg",width=200)
    

#----------------------------------------------------------------End----------------------------------------------------------------------------


