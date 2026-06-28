import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Airline System", layout="wide")

# -------- THEME --------
theme = st.sidebar.selectbox("🎨 Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    </style>
    """, unsafe_allow_html=True)

# -------- SIDEBAR --------
st.sidebar.title("✈ Airline System")

page = st.sidebar.radio(
    "📌 Navigation",
    ["📊 Dashboard", "➕ Booking", "📈 Analytics", "🌍 Travel Guide"]
)

# -------- DB --------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="airline_analytics"
)

# -------- LOAD DATA --------
df = pd.read_sql("""
SELECT b.booking_date, b.ticket_price, a.airline_name, f.flight_id
FROM bookings b
JOIN flights f ON b.flight_id = f.flight_id
JOIN airlines a ON f.airline_id = a.airline_id
""", conn)

df["booking_date"] = pd.to_datetime(df["booking_date"])

# -------- FILTERS --------
airlines = ["All"] + df["airline_name"].unique().tolist()

selected_airline = st.sidebar.selectbox("✈ Filter Airline", airlines)
selected_date = st.sidebar.date_input("📅 Filter Date")

filtered_df = df.copy()

if selected_airline != "All":
    filtered_df = filtered_df[filtered_df["airline_name"] == selected_airline]

if selected_date:
    filtered_df = filtered_df[
        filtered_df["booking_date"] <= pd.to_datetime(selected_date)
    ]

# ================= DASHBOARD =================
if page == "📊 Dashboard":
    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    total_rev = filtered_df['ticket_price'].sum()
    total_book = len(filtered_df)
    avg_price = filtered_df['ticket_price'].mean() or 0

    col1.metric("📋 Bookings", total_book)
    col2.metric("💰 Revenue", f"₹ {int(total_rev)}")
    col3.metric("📈 Avg Price", f"₹ {int(avg_price)}")

    # -------- BAR --------
    st.markdown("### ✈ Flights Distribution")
    dist = filtered_df.groupby("airline_name").size().reset_index(name="count")
    st.plotly_chart(px.bar(dist, x="airline_name", y="count", color="airline_name"), use_container_width=True)

    # -------- TREND --------
    st.markdown("### 📈 Revenue Trend")
    trend = filtered_df.groupby("booking_date")["ticket_price"].sum().reset_index()
    st.plotly_chart(px.line(trend, x="booking_date", y="ticket_price", markers=True), use_container_width=True)

    # -------- SMART ANALYSIS --------
    if len(trend) > 2:
        last = trend["ticket_price"].iloc[-1]
        prev = trend["ticket_price"].iloc[-2]

        change = ((last - prev) / prev) * 100 if prev != 0 else 0

        if change > 0:
            msg = f"🚀 Revenue Up by {change:.1f}% — Strong Growth!"
            color = "#00c853"
        elif change < 0:
            msg = f"⚠️ Revenue Down by {abs(change):.1f}% — Watch Loss!"
            color = "#d50000"
        else:
            msg = "😐 Revenue Stable"
            color = "#ffab00"

        # prediction (simple)
        future = trend["ticket_price"].rolling(2).mean().iloc[-1]

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg,{color},#000);
            padding:20px;
            border-radius:15px;
            color:white;
            margin-top:20px;
            text-align:center;
            font-size:18px;
        ">
        🤖 AI Insight <br><br>
        {msg} <br><br>
        🔮 Predicted Next Revenue: ₹ {int(future)}
        </div>
        """, unsafe_allow_html=True)

# ================= BOOKING =================
elif page == "➕ Booking":
    st.title("➕ Add Booking")

    passenger_id = st.number_input("Passenger ID", min_value=1)
    price = st.number_input("Ticket Price", min_value=0)
    date = st.date_input("Date")

    if st.button("Add Booking"):
        st.success("✅ Booking Added (Demo)")

# ================= ANALYTICS =================
elif page == "📈 Analytics":
    st.title("📈 Analytics")

    revenue_df = filtered_df.groupby("airline_name")["ticket_price"].sum().reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(px.bar(revenue_df, x="airline_name", y="ticket_price", color="airline_name"))

    with col2:
        st.plotly_chart(px.pie(revenue_df, names="airline_name", values="ticket_price"))

    top = revenue_df.sort_values("ticket_price", ascending=False).iloc[0]
    st.info(f"🏆 Top Airline: {top['airline_name']}")

# ================= TRAVEL GUIDE =================
elif page == "🌍 Travel Guide":

    st.title("🌍 Travel Guide")

    # -------- AI BOX --------
    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#667eea,#764ba2);
        padding:20px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">
    <h3>🤖 AI Travel Assistant</h3>
    <p>Tell me your vibe and I’ll suggest the best trip 😏✈️</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        budget = st.selectbox("💰 Budget", ["Low", "Medium", "High"])

    with col2:
        vibe = st.selectbox("🎯 Mood", ["Luxury", "Adventure", "Chill"])

    with col3:
        region = st.selectbox("🌍 Region", ["Asia", "Middle East", "Europe"])

    if st.button("✨ Get Suggestion"):

        if budget == "High" and vibe == "Luxury":
            suggestion = "Qatar Airways"
        elif vibe == "Adventure":
            suggestion = "Indigo"
        elif region == "Europe":
            suggestion = "Emirates"
        else:
            suggestion = "Air India"

        st.success(f"✈️ Suggested Airline: {suggestion}")

        ai_df = filtered_df[filtered_df["airline_name"] == suggestion]

        st.markdown("### 📈 Price Trend")
        trend = ai_df.groupby("booking_date")["ticket_price"].sum().reset_index()
        st.plotly_chart(px.line(trend, x="booking_date", y="ticket_price", markers=True))

        st.markdown("### ✈️ Available Flights")
        st.dataframe(ai_df.head(10))