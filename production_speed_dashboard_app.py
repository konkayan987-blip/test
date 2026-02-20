
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Production Speed Dashboard", layout="wide")

st.title("📊 Production Plan vs Speed Dashboard")

# โหลดข้อมูล
uploaded_file = st.file_uploader("อัปโหลดไฟล์ CSV ของคุณ", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔎 ข้อมูลทั้งหมด")
    st.dataframe(df)

    # ตรวจสอบคอลัมน์วันที่
    date_cols = [col for col in df.columns if "date" in col.lower() or "วัน" in col.lower()]
    
    if date_cols:
        date_col = date_cols[0]
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        st.sidebar.header("📅 ตัวกรองวันที่")
        min_date = df[date_col].min()
        max_date = df[date_col].max()

        start_date, end_date = st.sidebar.date_input(
            "เลือกช่วงวันที่",
            [min_date, max_date]
        )

        filtered_df = df[(df[date_col] >= pd.to_datetime(start_date)) & 
                         (df[date_col] <= pd.to_datetime(end_date))]
    else:
        filtered_df = df

    st.subheader("📈 กราฟวิเคราะห์")

    numeric_cols = filtered_df.select_dtypes(include='number').columns.tolist()

    if len(numeric_cols) >= 1:
        y_col = st.selectbox("เลือกคอลัมน์ตัวเลขที่ต้องการวิเคราะห์", numeric_cols)
        fig = px.line(filtered_df, x=filtered_df.index, y=y_col, title=f"Trend of {y_col}")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 สถิติ")
    st.write(filtered_df.describe())

else:
    st.info("กรุณาอัปโหลดไฟล์ CSV เพื่อเริ่มต้น")
