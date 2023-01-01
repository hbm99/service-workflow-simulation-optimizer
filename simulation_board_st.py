import pandas as pd 
from statistics import mean # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
from main import main



# ---- SIDEBAR ----
st.title("Simulated Shop Dashboard")
st.markdown("##")

peolple_at_section = [[0]]
tips_in_time = [0]

selected_customers = st.sidebar.multiselect(
    'Select the Customer Type:',
    ['ConsumeristCustomer', 'InAHurryCustomer', 'RegularCustomer'],
    ['ConsumeristCustomer', 'InAHurryCustomer', 'RegularCustomer']
)


st.sidebar.header("Please Filter Here:")

shop_size = st.sidebar.number_input("Shop size", min_value=10, step=5, help="Enter a shop size")

num_cashiers = st.sidebar.number_input("Cashier count", min_value=1, step=1, help= "Cashiers count should be approximately 10 percent of the shop size")

time = st.sidebar.number_input("Time", min_value=10, step=5, help="Enter time for simulation")
if time == "":
    time = 0

shelves_distribution = st.sidebar.text_input()

customer_types = []
customer_types.extend( customer.replace("'", "") for customer in selected_customers)

# ---- MAINPAGE ----

simulated_profits = [0]

if st.button("Star shop simulation"):
    if (shop_size != "") and (num_cashiers != "") and (time != ""):
        profits_in_time, peolple_at_section, tips_in_time = main(shop_size, num_cashiers, time, customer_types)
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

    st.area_chart(chart_people)

with medium_column:
    st.write("Shop profits in time")
    time = [str(i+1) for i in range(len(tips_in_time))]
    print(time)
     
    tips = pd.DataFrame({
    'index': time,
    'Tips': tips_in_time
    })

    tips = tips.set_index('index')

    st.bar_chart(tips)
    

with left_column:
    st.write("Shop profits in time")
    time = [str(i+1) for i in range(len(simulated_profits))]
    print(time)
     
    profits = pd.DataFrame({
    'index': time,
    'Profits': simulated_profits
    })

    profits = profits.set_index('index')

    st.line_chart(profits)
    




