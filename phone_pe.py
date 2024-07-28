import json
import requests
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as db
import pandas as pd
import plotly.express as px
from PIL import Image

#DataFrame Creation

#MySQL Connection
mydb = db.connect(
    host="localhost",
    port="3306",
    user="root",
    password="GovaMoni@Kanali26",
    database="phonepe_project")
mycursor = mydb.cursor()

#aggre_insurance_df
mycursor.execute("""SELECT * FROM aggregated_insurance""")
#mydb.commit()
table1 = mycursor.fetchall()

Aggre_insurance = pd.DataFrame(table1, columns = ("States", "Years", "Quarter", "Insurance_type", "Insurance_count","Insurance_amount"))

#aggre_transaction_df
mycursor.execute("""SELECT * FROM aggregated_transaction""")
#mydb.commit()
table2 = mycursor.fetchall()

Aggre_transaction = pd.DataFrame(table2, columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"))

#aggre_user_df
mycursor.execute("""SELECT * FROM aggregated_user""")
#mydb.commit()
table3 = mycursor.fetchall()

Aggre_user = pd.DataFrame(table3, columns = ("States", "Years", "Quarter", "Brands", "Transaction_count","Percentage"))

#map_insurance_df
mycursor.execute("""SELECT * FROM map_insurance""")
#mydb.commit()
table4 = mycursor.fetchall()

Map_insurance = pd.DataFrame(table4, columns = ("States", "Years", "Quarter", "District", "Transaction_count","Transaction_amount"))

#map_transaction_df
mycursor.execute("""SELECT * FROM map_transaction""")
#mydb.commit()
table5 = mycursor.fetchall()

Map_transaction = pd.DataFrame(table5, columns = ("States", "Years", "Quarter", "District", "Transaction_count","Transaction_amount"))

#map_user_df
mycursor.execute("""SELECT * FROM map_user""")
#mydb.commit()
table6 = mycursor.fetchall()

Map_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "District", "Registered_Users","App_Opens"))

#top_insurance_df
mycursor.execute("""SELECT * FROM top_insurance""")
#mydb.commit()
table7 = mycursor.fetchall()

Top_insurance = pd.DataFrame(table7, columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count","Transaction_amount"))

#top_transaction_df
mycursor.execute("""SELECT * FROM top_transaction""")
#mydb.commit()
table8 = mycursor.fetchall()

Top_transaction = pd.DataFrame(table8, columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count","Transaction_amount"))

#top_user_df
mycursor.execute("""SELECT * FROM top_user""")
#mydb.commit()
table9 = mycursor.fetchall()

Top_user = pd.DataFrame(table9, columns = ("States", "Years", "Quarter", "Pincodes", "Registered_Users"))



#Function for filtering year for Aggregated Insurance

def insurance_amount_count_Y(df, year):#[Iacy & Iacyg is dataframe]

    Iacy = df[df["Years"]==year] #Iacy["Years"].unique()
    Iacy.reset_index(drop=True, inplace=True)
    Iacyg = Iacy.groupby("States")[["Insurance_count", "Insurance_amount"]].sum()
    Iacyg.reset_index(inplace=True)

    #Plot creation
    #INSURANCE AMOUNT
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(Iacyg, x="States", y="Insurance_amount", title=f"{year} INSURANCE AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount)

 #INSURANCE COUNT
    with col2:
        fig_count = px.bar(Iacyg, x="States", y="Insurance_count", title=f"{year} INSURANCE COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_count)


    col1, col2 = st.columns(2)
    with col1:


        url ="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)

        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(Iacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color = "Insurance_amount", color_continuous_scale="Rainbow",
                                    range_color=(Iacyg["Insurance_amount"].min(), Iacyg["Insurance_amount"].max()),
                                    hover_name="States", title=f"{year} INSURANCE AMOUNT", fitbounds="locations", 
                                    height=600, width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(Iacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color = "Insurance_count", color_continuous_scale="Rainbow",
                                range_color=(Iacyg["Insurance_count"].min(), Iacyg["Insurance_count"].max()),
                                hover_name="States", title=f"{year} INSURANCE COUNT", fitbounds="locations", 
                                height=600, width=600)

        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return Iacy


#Function for Aggregated Insurance
#Function for quarter

def insurance_amount_count_Y_Q(df, quarter):
    Iacy = df[df["Quarter"]==quarter]
    Iacy.reset_index(drop=True, inplace=True)
    Iacyg = Iacy.groupby("States")[["Insurance_count", "Insurance_amount"]].sum()
    Iacyg.reset_index(inplace=True)


    #Plot creation
    #INSURANCE AMOUNT
    col1,col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(Iacyg, x="States", y="Insurance_amount", title=f"{Iacy["Years"].min()} YEAR {quarter} QUARTER INSURANCE AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)


    with col2:
    #INSURANCE COUNT
        fig_count = px.bar(Iacyg, x="States", y="Insurance_count", title=f"{Iacy["Years"].min()} YEAR {quarter} QUARTER INSURANCE COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:
        url ="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)

        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(Iacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color = "Insurance_amount", color_continuous_scale="Rainbow",
                                    range_color=(Iacyg["Insurance_amount"].min(), Iacyg["Insurance_amount"].max()),
                                    hover_name="States", title=f"{Iacy["Years"].min()} YEAR {quarter} QUARTER INSURANCE AMOUNT", fitbounds="locations",
                                    height=600, width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(Iacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color = "Insurance_count", color_continuous_scale="Rainbow",
                                range_color=(Iacyg["Insurance_count"].min(), Iacyg["Insurance_count"].max()),
                                hover_name="States", title=f"{Iacy["Years"].min()} YEAR {quarter} QUARTER INSURANCE COUNT", fitbounds="locations",
                                height=600, width=600)

        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    
    return Iacy


#Function for Aggregated Transaction for filtering years

def transaction_amount_count_Y(df, year):
    Tacy = df[df["Years"]==year]
    Tacy.reset_index(drop=True, inplace=True)
    Tacyg = Tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    Tacyg.reset_index(inplace=True)


    #Plot creation
    #TRANSACTION AMOUNT
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(Tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)


    #TRANSACTION COUNT
    with col2:
        fig_count = px.bar(Tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:
        url ="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)

        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(Tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale="Rainbow",
                                    range_color=(Tacyg["Transaction_amount"].min(), Tacyg["Transaction_amount"].max()),
                                    hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                    height=600, width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(Tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color = "Transaction_count", color_continuous_scale="Rainbow",
                                range_color=(Tacyg["Transaction_count"].min(), Tacyg["Transaction_count"].max()),
                                hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                height=600, width=600)

        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return Tacy


#Function for Aggregated Transaction
#Function for quarter
def transaction_amount_count_Y_Q(df, quarter):
    Tacy = df[df["Quarter"]==quarter] 
    Tacy.reset_index(drop=True, inplace=True)
    Tacyg = Tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    Tacyg.reset_index(inplace=True)


    #Plot creation
    #TRANSACTION AMOUNT
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(Tacyg, x="States", y="Transaction_amount", title=f"{Tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)


    #TRANSACTION COUNT
    with col2:
        fig_count = px.bar(Tacyg, x="States", y="Transaction_count", title=f"{Tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:

        url ="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)

        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(Tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale="Rainbow",
                                    range_color=(Tacyg["Transaction_amount"].min(), Tacyg["Transaction_amount"].max()),
                                    hover_name="States", title=f"{Tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                    height=600, width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(Tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color = "Transaction_count", color_continuous_scale="Rainbow",
                                range_color=(Tacyg["Transaction_count"].min(), Tacyg["Transaction_count"].max()),
                                hover_name="States", title=f"{Tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds="locations",
                                height=600, width=600)

        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    
    return Tacy

#function for transaction type
def aggre_trans_type(df, state):
    att = df[df["States"]== state]
    att.reset_index(drop=True, inplace=True)

    attg = att.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    attg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame= attg, names="Transaction_type", values= "Transaction_amount", width=600, title= f"{state.upper()} TRANSACTION_AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame= attg, names="Transaction_type", values= "Transaction_count", width=600, title= f"{state.upper()} TRANSACTION_COUNT", hole=0.5)
        st.plotly_chart(fig_pie_2)


#Aggree_User_analysis_1
def Aggre_user_plot_1(df, year):
    aguy = df[df["Years"] == year]
    aguy.reset_index(drop = True, inplace= True)

    aguyg = aguy.groupby("Brands")[["Transaction_count"]].sum()
    aguyg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyg, x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION_COUNT", width=800,
                       color_discrete_sequence=px.colors.sequential.haline_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggregated_user_analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq = df[df["Quarter"] == quarter]
    aguyq.reset_index(drop = True, inplace= True)


    aguyqg = aguyq.groupby("Brands")[["Transaction_count"]].sum()
    aguyqg.reset_index(inplace=True)

    fig_bar_2 = px.bar(aguyqg, x="Brands", y="Transaction_count", title=f"{quarter} QUARTER, BRANDS AND TRANSACTION_COUNT", width=800,
                        color_discrete_sequence=px.colors.sequential.Magenta_r, hover_name="Brands")
    st.plotly_chart(fig_bar_2)
    return aguyq


#Aggregated_User_Analysis_3
def Aggre_user_plot_3(df, state):
    auyqs = df[df["States"] == state]
    auyqs.reset_index(drop=True, inplace=True)

    fig_line_1 = px.line(auyqs, x="Brands", y="Transaction_count", hover_data="Percentage", title= f"{state.upper()} BRANDS_TRANSACTION COUNT_PERCENTAGE",
                         width=1000, markers=True)
    st.plotly_chart(fig_line_1)

#Map_Insurance_District
def map_insur_District(df, state):
    mid = df[df["States"]== state]
    mid.reset_index(drop=True, inplace=True)

    midg = mid.groupby("District")[["Transaction_count", "Transaction_amount"]].sum()
    midg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(midg, x="Transaction_amount", y= "District", orientation="h", height=600, title= f"{state.upper()} DISTRICT AND TRANSACTION_AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(midg, x="Transaction_count", y= "District", orientation="h", height=600, title= f"{state.upper()} DISTRICT AND TRANSACTION_COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)


#Map_User_analysis_1
def map_user_plot_1(df, year):
    muy = df[df["Years"] == year]
    muy.reset_index(drop = True, inplace= True)
    muyg = muy.groupby("States")[["Registered_Users", "App_Opens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1 = px.line(muyg, x="States", y=["Registered_Users", "App_Opens"], title= f"{year} REGISTERED_USERS, APP_OPENS", width=1000, height=800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy


#Map_User_analysis_2
def map_user_plot_2(df, quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop = True, inplace= True)
    muyqg = muyq.groupby("States")[["Registered_Users", "App_Opens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1 = px.line(muyqg, x="States", y=["Registered_Users", "App_Opens"], title= f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED_USERS, APP_OPENS",
                         width=1000, height=800, markers= True, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#Map_user_analysis_3
def map_user_plot_3(df, states):
    muyqs = df[df["States"] == states]
    muyqs.reset_index(drop = True, inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x="Registered_Users", y="District", orientation="h", title=f"{states.upper()} REGISTERED_USERS", height=800,
                                    color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2 = px.bar(muyqs, x="App_Opens", y="District", orientation="h", title=f"{states.upper()} APP_OPENS", height=800,
                                    color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)


#Top Insurance analysis
def top_ins_plot_1(df, state):
    tiy = df[df["States"] == state]
    tiy.reset_index(drop = True, inplace= True)

    col1,col2 = st.columns(2)
    with col1:
        fig_top_ins_bar_1 = px.bar(tiy, x="Quarter", y="Transaction_amount", hover_data="Pincodes", title= f"{state.upper()} TRANSACTION AMOUNT", height=650, width=600,
                                    color_discrete_sequence=px.colors.sequential.deep_r)
        st.plotly_chart(fig_top_ins_bar_1)

    with col2:
        fig_top_ins_bar_2 = px.bar(tiy, x="Quarter", y="Transaction_count", hover_data="Pincodes", title= f"{state.upper()} TRANSACTION COUNT", height=650, width=600,
                                    color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_top_ins_bar_2)

#Top user analysis
def top_user_plot_1(df, year):
    tuy = df[df["Years"] == year]
    tuy.reset_index(drop = True, inplace= True)

    tuyg = tuy.groupby(["States", "Quarter"])[["Registered_Users"]].sum()
    tuyg.reset_index(inplace=True)

    fig_top_user_bar_1=px.bar(tuyg, x="States", y="Registered_Users", color="Quarter", width=1000, height=800,
                            color_discrete_sequence= px.colors.sequential.Burgyl, hover_name="States", title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_user_bar_1)

    return tuy


#Top user analysis_2
def top_user_plot_2(df, state):
    tuys = df[df["States"]==state]
    tuys.reset_index(drop=True, inplace=True)


    fig_top_user_bar_2 = px.bar(tuys, x="Quarter", y="Registered_Users", title=f"{state} REGISTERED_USERS, PINCODES, QUARTER", width=1000, height=800, hover_data="Pincodes",
                                color="Registered_Users", color_continuous_scale=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_top_user_bar_2)


#Aggregated_Insurance_amount_Question1
def top_chart_insurance_amount(table_name):

    #MySQL Connection
    mydb = db.connect(
        host="localhost",
        port="3306",
        user="root",
        password="GovaMoni@Kanali26",
        database="phonepe_project")
    mycursor = mydb.cursor()

    #Plot_1
    query1 = f'''SELECT States, SUM(Insurance_amount) AS Insurance_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_amount desc
                LIMIT 10;'''
    mycursor.execute(query1)
    table1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table1, columns=("States", "Insurance_amount"))


    col1, col2 = st.columns(2)
    with col1:
        fig_amt1 = px.bar(df_1, x="States", y="Insurance_amount", title=f"{table_name.upper()} - TOP 10 OF INSURANCE AMOUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 600,width= 600)
        st.plotly_chart(fig_amt1)

    #Plot_2
    query2 = f'''SELECT States, SUM(Insurance_amount) AS Insurance_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_amount
                LIMIT 10;'''
    mycursor.execute(query2)
    table2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2, columns=("States", "Insurance_amount"))

    with col2:
        fig_amt2 = px.bar(df_2, x="States", y="Insurance_amount", title=f"{table_name.upper()} - LAST 10 OF INSURANCE AMOUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 600,width= 600)
        st.plotly_chart(fig_amt2)


    #Plot_3
    query3 = f'''SELECT States, AVG(Insurance_amount) AS Insurance_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_amount;'''
    mycursor.execute(query3)
    table3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3, columns=("States", "Insurance_amount"))

    fig_amt3 = px.bar(df_3, x="Insurance_amount", y="States", title=f"{table_name.upper()} - AVERAGE OF INSURANCE AMOUNT", hover_name="States", orientation="h",
                    color_discrete_sequence=px.colors.sequential.Blackbody_r, height= 800, width= 1000)
    st.plotly_chart(fig_amt3)


#Aggregated_insurance_count_Query1
def top_chart_insurance_count(table_name):

    #MySQL Connection
    mydb = db.connect(
        host="localhost",
        port="3306",
        user="root",
        password="GovaMoni@Kanali26",
        database="phonepe_project")
    mycursor = mydb.cursor()

    #Plot_1
    query1 = f'''SELECT States, SUM(Insurance_count) AS Insurance_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_count desc
                LIMIT 10;'''
    mycursor.execute(query1)
    table1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table1, columns=("States", "Insurance_count"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amt1 = px.bar(df_1, x="States", y="Insurance_count", title=f"{table_name.upper()} - TOP 10 OF INSURANCE COUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amt1)

    #Plot_2
    query2 = f'''SELECT States, SUM(Insurance_count) AS Insurance_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_count
                LIMIT 10;'''
    mycursor.execute(query2)
    table2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2, columns=("States", "Insurance_count"))

    with col2:
        fig_amt2 = px.bar(df_2, x="States", y="Insurance_count", title=f"{table_name.upper()} - LAST 10 OF INSURANCE COUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amt2)


    #Plot_3
    query3 = f'''SELECT States, AVG(Insurance_count) AS Insurance_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_count;'''
    mycursor.execute(query3)
    table3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3, columns=("States", "Insurance_count"))

    fig_amt3 = px.bar(df_3, x="Insurance_count", y="States", title=f"{table_name.upper()} - AVERAGE OF INSURANCE COUNT", hover_name="States", orientation="h",
                    color_discrete_sequence=px.colors.sequential.Blackbody_r, height= 700,width= 1000)
    st.plotly_chart(fig_amt3)


#Aggregated_Transaction_amount_Query1
def top_chart_transaction_amount(table_name):

    #MySQL Connection
    mydb = db.connect(
        host="localhost",
        port="3306",
        user="root",
        password="GovaMoni@Kanali26",
        database="phonepe_project")
    mycursor = mydb.cursor()

    #Plot_1
    query1 = f'''SELECT States, SUM(Transaction_amount) AS Transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount desc
                LIMIT 10;'''
    mycursor.execute(query1)
    table1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table1, columns=("States", "Transaction_amount"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amt1 = px.bar(df_1, x="States", y="Transaction_amount", title=f"{table_name.upper()} - TOP 10 TRANSACTION AMOUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amt1)

    #Plot_2
    query2 = f'''SELECT States, SUM(Transaction_amount) AS Transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount
                LIMIT 10;'''
    mycursor.execute(query2)
    table2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2, columns=("States", "Transaction_amount"))

    with col2:
        fig_amt2 = px.bar(df_2, x="States", y="Transaction_amount", title=f"{table_name.upper()} - LAST 10 OF TRANSACTION AMOUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amt2)


    #Plot_3
    query3 = f'''SELECT States, AVG(Transaction_amount) AS Transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount;'''
    mycursor.execute(query3)
    table3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3, columns=("States", "Transaction_amount"))

    fig_amt3 = px.bar(df_3, x="Transaction_amount", y="States", title=f"{table_name.upper()} - AVERAGE OF TRANSACTION AMOUNT", hover_name="States", orientation="h",
                    color_discrete_sequence=px.colors.sequential.Blackbody_r, height= 650,width= 600)
    st.plotly_chart(fig_amt3)

#Aggregated_Transaction_count_Query1
def top_chart_transaction_count(table_name):

    #MySQL Connection
    mydb = db.connect(
        host="localhost",
        port="3306",
        user="root",
        password="GovaMoni@Kanali26",
        database="phonepe_project")
    mycursor = mydb.cursor()

    #Plot_1
    query1 = f'''SELECT States, SUM(Transaction_count) AS Transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count desc
                LIMIT 10;'''
    mycursor.execute(query1)
    table1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table1, columns=("States", "Transaction_count"))

    col1,col2=st.columns(2)
    with col1:
        fig_amt1 = px.bar(df_1, x="States", y="Transaction_count", title=f"{table_name.upper()} - TOP 10 OF TRANSACTION COUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amt1)

    #Plot_2
    query2 = f'''SELECT States, SUM(Transaction_count) AS Transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count
                LIMIT 10;'''
    mycursor.execute(query2)
    table2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2, columns=("States", "Transaction_count"))
    with col2:
        fig_amt2 = px.bar(df_2, x="States", y="Transaction_count", title=f"{table_name.upper()} - LAST 10 OF TRANSACTION COUNT", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amt2)


    #Plot_3
    query3 = f'''SELECT States, AVG(Transaction_count) AS Transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count;'''
    mycursor.execute(query3)
    table3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3, columns=("States", "Transaction_count"))

    fig_amt3 = px.bar(df_3, x="Transaction_count", y="States", title=f"{table_name.upper()} - AVERAGE OF TRANSACTION COUNT", hover_name="States", orientation="h",
                    color_discrete_sequence=px.colors.sequential.Blackbody_r, height= 650,width= 600)
    st.plotly_chart(fig_amt3)


#Function for registered users
def top_chart_registered_users(table_name, state):

    #MySQL Connection
    mydb = db.connect(
        host="localhost",
        port="3306",
        user="root",
        password="GovaMoni@Kanali26",
        database="phonepe_project")
    mycursor = mydb.cursor()

    #Plot_1
    query1 = f'''SELECT District, SUM(Registered_Users) AS Registered_Users
                    FROM {table_name}
                    WHERE States = '{state}'
                    GROUP BY District
                    ORDER BY Registered_Users DESC
                    LIMIT 10;'''
    mycursor.execute(query1)
    table1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table1, columns=("District", "Registered_Users"))

    col1,col2=st.columns(2)
    with col1:
        fig_amt1 = px.bar(df_1, x="District", y="Registered_Users", title=f"{state.upper()} - TOP 10 OF REGISTERED USERS", hover_name="District",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amt1)

    #Plot_2
    query2 = f'''SELECT District, SUM(Registered_Users) AS Registered_Users
                    FROM {table_name}
                    WHERE States = '{state}'
                    GROUP BY District
                    ORDER BY Registered_Users
                    LIMIT 10;'''
    mycursor.execute(query2)
    table2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2, columns=("District", "Registered_Users"))

    with col2:
        fig_amt2 = px.bar(df_2, x="District", y="Registered_Users", title=f"{state.upper()} - LAST 10 OF REGISTERED USERS", hover_name="District",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amt2)


    #Plot_3
    query3 = f'''SELECT District, AVG(Registered_Users) AS Registered_Users
                    FROM {table_name}
                    WHERE States = '{state}'
                    GROUP BY District
                    ORDER BY Registered_Users;'''
    mycursor.execute(query3)
    table3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3, columns=("District", "Registered_Users"))

    fig_amt3 = px.bar(df_3, x="Registered_Users", y="District", title= f"{state.upper()} - AVERAGE OF REGISTERED USERS", hover_name="District", orientation="h",
                    color_discrete_sequence=px.colors.sequential.Blackbody_r, height= 650,width= 600)
    st.plotly_chart(fig_amt3)


#Function of app opens
def top_chart_app_opens(table_name, state):

    #MySQL Connection
    mydb = db.connect(
        host="localhost",
        port="3306",
        user="root",
        password="GovaMoni@Kanali26",
        database="phonepe_project")
    mycursor = mydb.cursor()

    #Plot_1
    query1 = f'''SELECT District, SUM(App_Opens) AS App_Opens
                    FROM {table_name}
                    WHERE States = '{state}'
                    GROUP BY District
                    ORDER BY App_Opens DESC
                    LIMIT 10;'''
    mycursor.execute(query1)
    table1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table1, columns=("District", "App_Opens"))
    col1, col2 = st.columns(2)
    with col1:
        fig_amt1 = px.bar(df_1, x="District", y="App_Opens", title=f"{state.upper()} - TOP 10 OF APP OPENS", hover_name="District",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amt1)

    #Plot_2
    query2 = f'''SELECT District, SUM(App_Opens) AS App_Opens
                    FROM {table_name}
                    WHERE States = '{state}'
                    GROUP BY District
                    ORDER BY App_Opens
                    LIMIT 10;'''
    mycursor.execute(query2)
    table2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2, columns=("District", "App_Opens"))

    with col2:
        fig_amt2 = px.bar(df_2, x="District", y="App_Opens", title=f"{state.upper()} - LAST 10 OF APP OPENS", hover_name="District",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amt2)


    #Plot_3
    query3 = f'''SELECT District, AVG(App_Opens) AS App_Opens
                    FROM {table_name}
                    WHERE States = '{state}'
                    GROUP BY District
                    ORDER BY App_Opens;'''
    mycursor.execute(query3)
    table3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3, columns=("District", "App_Opens"))

    fig_amt3 = px.bar(df_3, x="App_Opens", y="District", title=f"{state.upper()} - AVERAGE OF APP OPENS", hover_name="District", orientation="h",
                    color_discrete_sequence=px.colors.sequential.Blackbody_r, height= 650,width= 600)
    st.plotly_chart(fig_amt3)


#Fucntion for registered_users_top_user
def top_chart_registered_users_1(table_name):

    #MySQL Connection
    mydb = db.connect(
        host="localhost",
        port="3306",
        user="root",
        password="GovaMoni@Kanali26",
        database="phonepe_project")
    mycursor = mydb.cursor()

    #Plot_1
    query1 = f'''SELECT States, SUM(Registered_Users) AS Registered_Users
                    FROM {table_name}
                    GROUP BY States
                    ORDER BY Registered_Users DESC
                    LIMIT 10;'''
    mycursor.execute(query1)
    table1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table1, columns=("States", "Registered_Users"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amt1 = px.bar(df_1, x="States", y="Registered_Users", title=f"{table_name.upper()} - TOP 10 OF REGISTERED USERS", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amt1)

    #Plot_2
    query2 = f'''SELECT States, SUM(Registered_Users) AS Registered_Users
                    FROM {table_name}
                    GROUP BY States
                    ORDER BY Registered_Users
                    LIMIT 10;'''
    mycursor.execute(query2)
    table2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2, columns=("States", "Registered_Users"))

    with col2:
        fig_amt2 = px.bar(df_2, x="States", y="Registered_Users", title=f"{table_name.upper()} - LAST 10 OF REGISTERED USERS", hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amt2)


    #Plot_3
    query3 = f'''SELECT States, AVG(Registered_Users) AS Registered_Users
                    FROM {table_name}
                    GROUP BY States
                    ORDER BY Registered_Users;'''
    mycursor.execute(query3)
    table3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3, columns=("States", "Registered_Users"))

    fig_amt3 = px.bar(df_3, x="Registered_Users", y="States", title=f"{table_name.upper()} - AVERAGE OF REGISTERED USERS", hover_name="States", orientation="h",
                    color_discrete_sequence=px.colors.sequential.Blackbody_r, height= 650,width= 600)
    st.plotly_chart(fig_amt3)




















#Streamlit

st.set_page_config(layout="wide")

st.image("phone_pe_logo.png", width=200)
st.title(":blue[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]")

with st.sidebar:
    select = option_menu("Main Menu",
                      ["HOME", "DATA EXPLORATION", "TOP CHARTS"],
                      icons=["house", "database", "bar-chart-line"])

if select == "HOME":
    
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    with col2:
        st.image(Image.open("D:/Gova/Data Science Course/Projects/2.Phonepe_Pulse_Data_Visualization/phone_pe_logo_1"), width=600)

    
    col3,col4= st.columns(2)
    
    with col3:
        st.video("D:\\Gova\\Data Science Course\\Projects\\2.Phonepe_Pulse_Data_Visualization\\Introducing PhonePe Pulse.mp4")


    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open("D:/Gova/Data Science Course/Projects/2.Phonepe_Pulse_Data_Visualization/phone_pe_logo.png"), width=600)


elif select == "DATA EXPLORATION":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method_1 = st.radio("Select the method", ["Insurance_Analysis", "Transaction_Analysis", "User_Analysis"])

        if method_1 == "Insurance_Analysis":

            col1, col2 = st.columns(2)
            with col1:
                years= st.slider("Select the year", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(), Aggre_insurance["Years"].min())
            Iac_Y=insurance_amount_count_Y(Aggre_insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the quarter", Iac_Y["Quarter"].min(), Iac_Y["Quarter"].max(), Iac_Y["Quarter"].min())
            insurance_amount_count_Y_Q(Iac_Y, quarters)

        elif method_1 == "Transaction_Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                years= st.slider("Select the year", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(), Aggre_transaction["Years"].min())
            A_Tac_Y=transaction_amount_count_Y(Aggre_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select a state", A_Tac_Y["States"].unique())
            aggre_trans_type(A_Tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the quarter", A_Tac_Y["Quarter"].min(), A_Tac_Y["Quarter"].max(), A_Tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q = transaction_amount_count_Y_Q(A_Tac_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select a state_ty", Aggre_tran_tac_Y_Q["States"].unique())
            aggre_trans_type(Aggre_tran_tac_Y_Q, states)


        elif method_1 == "User_Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years= st.slider("Select the year", Aggre_user["Years"].min(), Aggre_user["Years"].max(), Aggre_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot_1(Aggre_user, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the quarter", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select a state", Aggre_user_Y_Q["States"].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q, states)


    with tab2:
        method_2 = st.radio("Select the method", ["Map_Insurance_Analysis", "Map_Transaction_Analysis", "Map_User_Analysis"])

        if method_2 == "Map_Insurance_Analysis":

            col1, col2 = st.columns(2)
            with col1:
                years= st.slider("Select the year_MI", Map_insurance["Years"].min(), Map_insurance["Years"].max(), Map_insurance["Years"].min())
            M_Ins_Y=transaction_amount_count_Y(Map_insurance, years)


            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select a state_MI", M_Ins_Y["States"].unique())
            map_insur_District(M_Ins_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the quarter_MI", M_Ins_Y["Quarter"].min(), M_Ins_Y["Quarter"].max(), M_Ins_Y["Quarter"].min())
            M_Ins_Y_Q = transaction_amount_count_Y_Q(M_Ins_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select a state_MIA", M_Ins_Y_Q["States"].unique())
            map_insur_District(M_Ins_Y_Q, states)
            

        elif method_2 == "Map_Transaction_Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                years= st.slider("Select the year_MT", Map_transaction["Years"].min(), Map_transaction["Years"].max(), Map_transaction["Years"].min())
            M_Tran_Y=transaction_amount_count_Y(Map_transaction, years)


            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select a state_MT", M_Tran_Y["States"].unique())
            map_insur_District(M_Tran_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the quarter_MT", M_Tran_Y["Quarter"].min(), M_Tran_Y["Quarter"].max(), M_Tran_Y["Quarter"].min())
            M_Tran_Y_Q = transaction_amount_count_Y_Q(M_Tran_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select a state_MTA", M_Tran_Y_Q["States"].unique())
            map_insur_District(M_Tran_Y_Q, states)



        elif method_2 == "Map_User_Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years= st.slider("Select the year_MU", Map_user["Years"].min(), Map_user["Years"].max(), Map_user["Years"].min())
            M_user_Y=map_user_plot_1(Map_user, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the quarter_MU", M_user_Y["Quarter"].min(), M_user_Y["Quarter"].max(), M_user_Y["Quarter"].min())
            M_user_Y_Q = map_user_plot_2(M_user_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select a state_MU", M_user_Y_Q["States"].unique())
            map_user_plot_3(M_user_Y_Q, states)





    with tab3:
        method_3 = st.radio("Select the method", ["Top_Insurance_Analysis", "Top_Transaction_Analysis", "Top_User_Analysis"])

        if method_3 == "Top_Insurance_Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years= st.slider("Select the year_TI", Top_insurance["Years"].min(), Top_insurance["Years"].max(), Top_insurance["Years"].min())
            T_Ins_Y=transaction_amount_count_Y(Top_insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select a state_TI", T_Ins_Y["States"].unique())
            top_ins_plot_1(T_Ins_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the quarter_TI", T_Ins_Y["Quarter"].min(), T_Ins_Y["Quarter"].max(), T_Ins_Y["Quarter"].min())
            T_ins_Y_Q = transaction_amount_count_Y_Q(T_Ins_Y, quarters)



        elif method_3 == "Top_Transaction_Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years= st.slider("Select the year_TT", Top_transaction["Years"].min(), Top_transaction["Years"].max(), Top_transaction["Years"].min())
            T_Tran_Y=transaction_amount_count_Y(Top_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select a state_TT", T_Tran_Y["States"].unique())
            top_ins_plot_1(T_Tran_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the quarter_TT", T_Tran_Y["Quarter"].min(), T_Tran_Y["Quarter"].max(), T_Tran_Y["Quarter"].min())
            T_Tran_Y_Q = transaction_amount_count_Y_Q(T_Tran_Y, quarters)



        elif method_3 == "Top_User_Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years= st.slider("Select the year_TU", Top_user["Years"].min(), Top_user["Years"].max(), Top_user["Years"].min())
            T_User_Y=top_user_plot_1(Top_user, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select a state_TU", T_User_Y["States"].unique())
            top_user_plot_2(T_User_Y, states)


elif select == "TOP CHARTS":
    questions = st.selectbox("Select the Question", ["1. Transaction Amount and Count of Aggregated Insurance",
                                                        "2. Transaction Amount and Count of Map Insurance",
                                                        "3. Transaction Amount and Count of Top Insurance",
                                                        "4. Transaction Amount and Count of Aggregated Transaction",
                                                        "5. Transaction Amount and Count of Map Transaction",
                                                        "6. Transaction Amount and Count of Top Transaction",
                                                        "7. Transaction Count of Aggregated User",
                                                        "8. Registered Users of Map User",
                                                        "9. App Opens of Map User",
                                                        "10. Registered Users of Top User"])
    
    if questions == "1. Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("INSURANCE AMOUNT")
        top_chart_insurance_amount("aggregated_insurance")
        st.subheader("INSURANCE COUNT")
        top_chart_insurance_count("aggregated_insurance")


    elif questions == "2. Transaction Amount and Count of Map Insurance":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif questions == "3. Transaction Amount and Count of Top Insurance":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif questions == "4. Transaction Amount and Count of Aggregated Transaction":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif questions == "5. Transaction Amount and Count of Map Transaction":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif questions == "6. Transaction Amount and Count of Top Transaction":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif questions == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif questions == "8. Registered Users of Map User":

        states=st.selectbox("Select the state", Map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("map_user", states)

    elif questions == "9. App Opens of Map User":

        states=st.selectbox("Select the state", Map_user["States"].unique())
        st.subheader("APP OPENS")
        top_chart_app_opens("map_user", states)

    elif questions == "10. Registered Users of Top User":

        st.subheader("REGISTERED USERS")
        top_chart_registered_users_1("top_user")