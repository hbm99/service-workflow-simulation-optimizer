import pandas as pd 
from statistics import mean # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
import regex as re
from main import main



# ---- SIDEBAR ----
st.markdown("######")
st.title("Shop's simulation optimization")

peolple_at_section = [[0]]
tips_in_time = [0]

st.sidebar.header("Enter parameters value")

shop_size = st.sidebar.number_input("Shop size", min_value=10, step=5, help="Enter a shop size")

num_cashiers = st.sidebar.number_input("Cashier count", min_value=1, value=2, step=1, help= "Cashiers count should be approximately 10 percent of the shop size")

time = st.sidebar.number_input("Time", min_value=10, value=3600, step=5, help="Enter time for simulation")

shelves_count = st.sidebar.number_input("Shelves count", min_value=2, value=4, step=1, help="Count of shelves at the shop")

iterations = st.sidebar.number_input("Iterations", min_value=3, value=6, step=1, help="Number of iterations for Tabu Search algorithm")

sim_num = st.sidebar.number_input("Simulations number", min_value=1, step=1, help="Count of simulations")


# ---- MAINPAGE ----

solutions_fit = []
results = ""

if st.button("Start shop's simulation optimization"):
    results, solutions_fit = main(shop_size, num_cashiers, time, shelves_count, iterations, sim_num)

    for i in range(len(solutions_fit)):
        distribution = solutions_fit[i].keys()
        profits = solutions_fit[i].values()
    
    #reg_result = re.compile('[\S]')

    #results = reg_result.search(str(results)

    st.markdown(f'Best solution found: **{results[0][0]}**')
    st.markdown(f'Value: **{results[0][1]}**')

    st.write("Profits for a shelves distributuin")
    
    profits = pd.DataFrame({
    'Shelves distribution': distribution,
    'Profits': profits
    })

    profits = profits.set_index('Shelves distribution')

    st.line_chart(profits)
