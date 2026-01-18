import pandas as pd
import streamlit as st

st.set_page_config(page_title="Penguins Dashboard", layout="wide")
st.title("🐧 Penguins Dashboard")

# ===== Load data =====
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
df = pd.read_csv(url)

# ===== Sidebar: เลือกเพศ =====
with st.sidebar:
    st.header("Filter")
    sex_list = sorted(df["sex"].dropna().unique())

    selected_sex = st.multiselect(
        "เลือกเพศ (Sex)",
        sex_list,
        default=sex_list
    )

# ===== Filter dataframe =====
df_filtered = (
    df if len(selected_sex) == 0
    else df[df["sex"].isin(selected_sex)]
)

# ===== Clean data =====
df_clean = df_filtered.dropna(
    subset=["sex", "species", "body_mass_g", "flipper_length_mm"]
)

# ===== Prepare data =====
mass_by_sex = (
    df_clean
    .groupby("sex", as_index=False)["body_mass_g"]
    .mean()
)

flipper_by_sex = (
    df_clean
    .groupby("sex", as_index=False)["flipper_length_mm"]
    .mean()
)

# ===== Layout: columns =====
col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Body Mass by Sex")
    st.bar_chart(mass_by_sex, x="sex", y="body_mass_g")

with col2:
    st.subheader("Average Flipper Length by Sex")
    st.bar_chart(flipper_by_sex, x="sex", y="flipper_length_mm")

# ===== Layout: tabs =====
tab1, tab2, tab3 = st.tabs(["🐧 Body Mass", "🪽 Flipper Length", "📊 Raw Data"])

with tab1:
    st.subheader("Average Body Mass by Sex")
    st.bar_chart(mass_by_sex, x="sex", y="body_mass_g")

with tab2:
    st.subheader("Average Flipper Length by Sex")
    st.bar_chart(flipper_by_sex, x="sex", y="flipper_length_mm")

with tab3:
    st.subheader("Filtered Penguins Dataset")
    st.dataframe(df_clean, use_container_width=True)
