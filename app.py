import streamlit as st
import numpy as np
import pandas as pd
import pickle

st.title("Car Price Prediction App")
df = pd.read_csv("final_data.csv")
model = pickle.load(open("model.pkl", "rb"))

companies = sorted(df['company'].unique())
company = st.sidebar.selectbox("Select company", companies)

names = sorted(df[df['company'] == company]['name'].unique())

name = st.sidebar.selectbox("Select name", names)
year = st.sidebar.number_input("Enter year", min_value = 2000, max_value = 2026, step = 1)
km_driven = st.sidebar.number_input("Enter km driven", value = 50000, min_value = 1000, max_value = 200000, step = 5000)
fuel_type = st.sidebar.selectbox("Select fuel type", ["Petrol", "Diesel"])

if st.sidebar.button("Predict Price"):
    st.write("Predicting for")
    st.write("Company: ", company)
    st.write("Name: ", name)
    st.write("Year: ", str(year))
    st.write("KM Driven: ", str(km_driven))
    st.write("Fuel Type: ", fuel_type)

    columns = ['company', 'name', 'year', 'kms_driven', 'fuel_type']
    myinput = [[company, name, year, km_driven, fuel_type]]
    myinput = pd.DataFrame(data = myinput, columns = columns)
    #st.write(myinput)
    result = model.predict(myinput)
    if result[0,0] < 0:
        st.error("Sorry, inputs are wrong.")
    else:
        st.success("Predicted Price:" + str(round(result[0,0])))
