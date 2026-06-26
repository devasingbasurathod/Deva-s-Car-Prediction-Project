import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}

[data-testid="stSidebar"]{
    background:#111827;
}

.main-card{
    background:rgba(255,255,255,0.08);
    padding:25px;
    border-radius:20px;
    backdrop-filter:blur(12px);
    box-shadow:0px 8px 25px rgba(0,0,0,0.4);
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

.stButton>button{
    width:100%;
    background:linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    border:none;
    border-radius:12px;
    padding:12px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    transform:scale(1.03);
}

.price{
    font-size:42px;
    color:#00ff88;
    font-weight:bold;
    text-align:center;
    margin-top:20px;
}

.footer{
    text-align:center;
    color:white;
    margin-top:50px;
    opacity:0.7;
}

</style>
""", unsafe_allow_html=True)

df = pd.read_csv("final_data.csv")
model = pickle.load(open("model.pkl", "rb"))

st.markdown("<h1>🚗 Online Car Price Prediction</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="main-card">
<h3>Predict the resale price of your used car</h3>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🚘 Car Details")

companies = sorted(df["company"].unique())

company = st.sidebar.selectbox(
    "Company",
    companies
)

names = sorted(df[df["company"] == company]["name"].unique())

name = st.sidebar.selectbox(
    "Model",
    names
)

year = st.sidebar.number_input(
    "Manufacturing Year",
    min_value=2000,
    max_value=2026,
    step=1
)

km_driven = st.sidebar.number_input(
    "KM Driven",
    min_value=1000,
    max_value=200000,
    value=50000,
    step=5000
)

fuel_type = st.sidebar.selectbox(
    "Fuel Type",
    ["Petrol", "Diesel"]
)

st.sidebar.markdown("---")

predict = st.sidebar.button("💰 Predict Price")

col1, col2 = st.columns(2)

with col1:
    st.metric("Company", company)

with col2:
    st.metric("Fuel Type", fuel_type)

if predict:

    myinput = pd.DataFrame(
        [[company, name, year, km_driven, fuel_type]],
        columns=[
            "company",
            "name",
            "year",
            "kms_driven",
            "fuel_type"
        ]
    )

    result = model.predict(myinput)

    if result[0,0] < 0:
        st.error("❌ Invalid Input")
    else:
        price = round(result[0,0])

        st.success("Prediction Completed Successfully")

        st.markdown(
            f"<div class='price'>₹ {price:,}</div>",
            unsafe_allow_html=True
        )

        st.write("### 📋 Car Details")

        c1, c2 = st.columns(2)

        with c1:
            st.info(f"""
**Company**

{company}

**Model**

{name}

**Year**

{year}
""")

        with c2:
            st.info(f"""
**KM Driven**

{km_driven:,}

**Fuel Type**

{fuel_type}
""")

st.markdown("""
<div class="footer">
Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
