import pandas as pd 
from statistics import mean # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
from main import main



# ---- SIDEBAR ----
st.title("Simulated Shop Dashboard")
st.markdown("##")

peolple_at_section = [[0, 0, 0],[0, 0, 0],[0,0,0]]

st.sidebar.header("Please Filter Here:")

left_column, medium_column, right_column = st.columns(3)
with left_column:
    shop_size = st.text_input("Shop size", placeholder="Enter a shop size")

with medium_column:
    num_cashiers = st.text_input("Cashier count", help= "Cashiers count should be approximately 10 percent of the shop size", 
                                                    placeholder="Enter a cashiers count")

with right_column:
    time = st.text_input( "Time (sec)" ,placeholder="Enter time for simulation (sec)")
    if time == "":
        time = 0

selected_customers = st.sidebar.multiselect(
    'Select the Customer Type:',
    ['ConsumeristCustomer', 'InAHurryCustomer', 'RegularCustomer'],
    ['ConsumeristCustomer', 'InAHurryCustomer', 'RegularCustomer']
)

customer_types = []
customer_types.extend( customer.replace("'", "") for customer in selected_customers)

# ---- MAINPAGE ----

simulated_profits = [0]

if st.button("Star shop simulation"):
    if (shop_size != "") and (num_cashiers != "") and (time != ""):
        profits_in_time, peolple_at_section, tips_in_time = main(int(shop_size), int(num_cashiers), int(time), customer_types)
        simulated_profits = profits_in_time

    else:
        st.write("Please, complete de parameters for the simulation")


average_profits = round(mean(simulated_profits), 2)
total_profits = simulated_profits[-1]

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Profits:")
    st.subheader(f"$ {total_profits:,}")
with right_column:
    st.subheader("Average Profits:")
    st.subheader(f"$ {average_profits}")

st.markdown("""---""")


left_column, medium_column, right_column = st.columns(3)
with right_column:
    st.write("Count of people at each section all over the time")
    cols = [str(i+1) for i in range(len(peolple_at_section[0]))]
    chart_people = pd.DataFrame(
        peolple_at_section,
        columns=cols)

    st.line_chart(chart_people)

#with medium_column:
    #cols = []

with left_column:
    st.write("Shop profits in time")
    time = [str(i+1) for i in range(len(simulated_profits))]
    print(time)
     
    df = pd.DataFrame({
    'Time': time,
    'Profits': simulated_profits
    })

    df = df.rename(columns={'Time':'index'}).set_index('index')
    print(df['Time'])

    st.bar_chart(df)
    




