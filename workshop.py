import pandas as pd
import streamlit as st

st.title("My First Streamlit App")
st.header("Hello, welcome to my app!")
st.write("This is a simple Streamlit application.")

#link = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/car_crashes.csv"
#df = pd.read_csv(link)


df = pd.read_csv("datasets/1642645053.csv", encoding="tis-620")

st.write(df)

number = st.slider("Select a number", 0, 100, 50)
st.write("The current number is ", number)

rating = st.radio(
    "How would you rate this class?",
    ("1", "2", "3", "4", "5")
)
st.write(f"You selected {rating}")

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    st.checkbox("Disable selectbox widget", key="disabled")
    st.radio(
        "Set selectbox label visibility 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )

with col2:
    option = st.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"

df = pd.read_csv(url)
df_grouped_by_species = df.groupby("species")["body_mass_g"].mean()
st.bar_chart(df_grouped_by_species)