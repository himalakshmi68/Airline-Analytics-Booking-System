import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Airline System", layout="wide")

theme = st.sidebar.selectbox("🎨 Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    h1,h2,h3,p,span,div { color:white !important; }
    </style>
    """, unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["✈ Airline System", "👤 Passenger Hub"])

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="airline_analytics"
)

df = pd.read_sql("""
SELECT b.booking_date, b.ticket_price, a.airline_name, f.flight_id
FROM bookings b
JOIN flights f ON b.flight_id = f.flight_id
JOIN airlines a ON f.airline_id = a.airline_id
""", conn)

df["booking_date"] = pd.to_datetime(df["booking_date"])

airlines = ["All"] + df["airline_name"].unique().tolist()

selected_airline = st.sidebar.selectbox("✈ Filter Airline", airlines)
selected_date = st.sidebar.date_input("📅 Filter Date")

filtered_df = df.copy()

if selected_airline != "All":
    filtered_df = filtered_df[filtered_df["airline_name"] == selected_airline]

if selected_date:
    filtered_df = filtered_df[
        filtered_df["booking_date"].dt.date <= selected_date
    ]

if page == "✈ Airline System":

    st.title("✈ Airline System Dashboard")

    if filtered_df.empty:
        st.warning("No data available for selected filters")
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("📋 Bookings", len(filtered_df))
        col2.metric("💰 Revenue", f"₹ {int(filtered_df['ticket_price'].sum())}")
        col3.metric("✈ Departures", len(filtered_df))

        top_airline = filtered_df["airline_name"].value_counts().idxmax()
        st.success(f"🏆 Top Airline: {top_airline}")

        trend_pass = filtered_df.groupby("booking_date").size().reset_index(name="count")

        if len(trend_pass) > 1:
            if trend_pass["count"].iloc[-1] > trend_pass["count"].iloc[-2]:
                st.success("📈 Passenger Increase")
            elif trend_pass["count"].iloc[-1] < trend_pass["count"].iloc[-2]:
                st.error("📉 Passenger Decrease")
            else:
                st.info("😐 No Change")

        rev_trend = filtered_df.groupby("booking_date")["ticket_price"].sum().reset_index()

        if len(rev_trend) > 1:
            last = rev_trend["ticket_price"].iloc[-1]
            prev = rev_trend["ticket_price"].iloc[-2]

            change = ((last - prev) / prev) * 100 if prev != 0 else 0

            if change > 0:
                st.success(f"🚀 Profit Up {change:.1f}%")
            else:
                st.error(f"⚠️ Loss Down {abs(change):.1f}%")

        st.markdown("---")

        st.header("📈 Analytics")

        revenue_df = filtered_df.groupby("airline_name")["ticket_price"].sum().reset_index()

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                px.bar(revenue_df, x="airline_name", y="ticket_price", color="airline_name"),
                use_container_width=True
            )

        with col2:
            st.plotly_chart(
                px.pie(revenue_df, names="airline_name", values="ticket_price"),
                use_container_width=True
            )

        st.plotly_chart(
            px.line(rev_trend, x="booking_date", y="ticket_price", markers=True),
            use_container_width=True
        )

        st.plotly_chart(
            px.line(trend_pass, x="booking_date", y="count", markers=True),
            use_container_width=True
        )

elif page == "👤 Passenger Hub":

    st.title("👤 Passenger Hub")

    if filtered_df.empty:
        st.warning("No data available")
    else:
        st.subheader("🤖 Travel Guide")

        col1, col2, col3 = st.columns(3)

        with col1:
            budget = st.selectbox("💰 Budget", ["Low", "Medium", "High"])
        with col2:
            vibe = st.selectbox("🎯 Mood", ["Luxury", "Adventure", "Chill"])
        with col3:
            region = st.selectbox("🌍 Region", ["Asia", "Middle East", "Europe"])

        if st.button("✨ Get Suggestion"):

            if budget == "High":
                suggestion = "Qatar Airways"
            elif vibe == "Adventure":
                suggestion = "Indigo"
            elif region == "Europe":
                suggestion = "Emirates"
            else:
                suggestion = "Air India"

            st.success(f"✈️ Suggested Airline: {suggestion}")

            ai_df = filtered_df[filtered_df["airline_name"] == suggestion]

            if not ai_df.empty:
                st.plotly_chart(
                    px.line(
                        ai_df.groupby("booking_date")["ticket_price"].sum().reset_index(),
                        x="booking_date",
                        y="ticket_price",
                        markers=True
                    ),
                    use_container_width=True
                )
            else:
                st.warning("No data for this airline")

        st.subheader("📋 My Bookings")
        st.dataframe(filtered_df.head(10))

        st.subheader("💡 Smart Advice")

        rev_trend = filtered_df.groupby("booking_date")["ticket_price"].sum().reset_index()

        if len(rev_trend) > 1:
            if rev_trend["ticket_price"].iloc[-1] > rev_trend["ticket_price"].iloc[-2]:
                st.warning("💸 Prices increasing — Book Now!")
            else:
                st.success("🟢 Prices dropping — Wait for better deal!")