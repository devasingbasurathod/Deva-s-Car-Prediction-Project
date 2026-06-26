import streamlit as st
import numpy as np
import pandas as pd
import pickle

st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}

.main-card{
    background: rgba(255,255,255,0.08);
    padding:30px;
    border-radius:20px;
    backdrop-filter: blur(10px);
    box-shadow:0px 10px 30px rgba(0,0,0,0.4);
}

h1{
    text-align:center;
    color:white;
}

h3{
    color:white;
}

label{
    color:white !important;
    font-weight:bold;
}

[data-testid="stSidebar"]{
    background:#111827;
}

.stButton>button{
    width:100%;
    background:linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    font-size:18px;
    border:none;
    border-radius:12px;
    padding:10px;
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.05);
}

.price{
    text-align:center;
    color:#00ff88;
    font-size:40px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

df = pd.read_csv("final_data.csv")
model = pickle.load(open("model.pkl","rb"))

st.markdown("<h1>🚗 Online Car Price Prediction</h1>", unsafe_allow_html=True)

st.markdown(
"""
<div class="main-card">
<h3>Enter Car Details</h3>
</div>
""",
unsafe_allow_html=True
)

companies = sorted(df["company"].unique())

company = st.sidebar.selectbox("🏢 Company", companies)

names = sorted(df[df["company"] == company]["name"].unique())

name = st.sidebar.selectbox("🚘 Model", names)

year = st.sidebar.number_input(
    "📅 Manufacturing Year",
    min_value=2000,
    max_value=2026,
    step=1
)

km_driven = st.sidebar.number_input(
    "🛣 KM Driven",
    value=50000,
    min_value=1000,
    max_value=200000,
    step=5000
)

fuel_type = st.sidebar.selectbox(
    "⛽ Fuel Type",
    ["Petrol","Diesel"]
)

col1,col2 = st.columns(2)

with col1:
    st.metric("Selected Company", company)

with col2:
    st.metric("Fuel Type", fuel_type)

if st.button("💰 Predict Price"):

    columns = [
        "company",
        "name",
        "year",
        "kms_driven",
        "fuel_type"
    ]

    myinput = pd.DataFrame(
        [[company,name,year,km_driven,fuel_type]],
        columns=columns
    )

    result = model.predict(myinput)

    if result[0,0] < 0:
        st.error("❌ Invalid Input")
    else:
        price = round(result[0,0])

        st.balloons()

        st.success("Prediction Completed")

        st.markdown(
            f"<div class='price'>₹ {price:,}</div>",
            unsafe_allow_html=True
        )

        st.info(f"""
**Car Details**

🚗 Company : {company}

🚘 Model : {name}

📅 Year : {year}

🛣 KM Driven : {km_driven:,}

⛽ Fuel : {fuel_type}
""")
