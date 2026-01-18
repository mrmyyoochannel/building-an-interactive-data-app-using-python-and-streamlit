import pandas as pd
import streamlit as st
import plotly.express as px

# ===============================
# Page config
# ===============================
st.set_page_config(page_title="ข้อมูลปศุสัตว์ไทย 2564", layout="wide")
st.title("🐄 ภาพรวมข้อมูลปศุสัตว์ไทย ปี 2564")
st.caption("แหล่งข้อมูล: กรมปศุสัตว์")

# ===============================
# Load data
# ===============================
df = pd.read_csv("datasets/1642645053.csv", encoding="tis-620")

province_col = "สถานที่เลี้ยงสัตว์ จังหวัด"

# 🔧 เลือกคอลัมน์ตัวเลขที่ใช้วิเคราะห์ (เพิ่มได้)
value_columns = [
    "โคเนื้อ พื้นเมือง เพศผู้ (ตัว)",
]

# ===============================
# Sidebar filters
# ===============================
st.sidebar.header("🔍 ตัวกรองข้อมูล")

provinces = sorted(df[province_col].dropna().unique())
selected_provinces = st.sidebar.multiselect(
    "เลือกจังหวัด",
    provinces,
    placeholder="เลือกได้มากกว่า 1 จังหวัด"
)

selected_values = st.sidebar.multiselect(
    "เลือกตัวแปรที่ต้องการวิเคราะห์",
    value_columns,
    default=value_columns
)

agg_method = st.sidebar.radio(
    "เลือกวิธีคำนวณ",
    ["sum", "mean", "median"],
    index=1
)

top5_only = st.sidebar.checkbox("แสดง Top 5 จังหวัด")

# ===============================
# Filter จังหวัด
# ===============================
filtered_df = (
    df if len(selected_provinces) == 0
    else df[df[province_col].isin(selected_provinces)]
)

# ===============================
# Load lat / lon
# ===============================
provinces_df = pd.read_csv(
    "https://raw.githubusercontent.com/dataengineercafe/thailand-province-latitude-longitude/main/provinces.csv"
)

# ===============================
# วิเคราะห์ทีละตัวแปร
# ===============================
for value_col in selected_values:

    st.divider()
    st.header(f"📊 {value_col}")

    # ----- Clean data -----
    clean_df = filtered_df[[province_col, value_col]].dropna()
    clean_df[value_col] = (
        clean_df[value_col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(int)
    )

    # ----- Aggregate -----
    grouped_df = (
        clean_df
        .groupby(province_col)[value_col]
        .agg(agg_method)
        .reset_index()
        .rename(columns={value_col: "value"})
    )

    # ----- Top 5 -----
    if top5_only:
        grouped_df = grouped_df.sort_values("value", ascending=False).head(5)

    # ----- Metric -----
    st.metric(
        label=f"ค่า {agg_method}",
        value=f"{grouped_df['value'].mean():,.0f}"
    )

    col1, col2 = st.columns(2)

    # ----- Bar chart -----
    with col1:
        fig = px.bar(
            grouped_df,
            x=province_col,
            y="value",
            labels={
                province_col: "จังหวัด",
                "value": f"{agg_method} (ตัว)"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    # ----- Map -----
    with col2:
        map_df = pd.merge(
            grouped_df,
            provinces_df,
            left_on=province_col,
            right_on="province_name",
            how="inner"
        )

        st.map(
            map_df,
            latitude="province_lat",
            longitude="province_lon",
            size="value"
        )

    # ----- Table -----
    st.subheader("📄 ตารางข้อมูล")
    st.dataframe(grouped_df, use_container_width=True)
