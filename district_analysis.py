# district_visualization.py

import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

def visualize_district_transactions():
    """
    Streamlit app to visualize district-wise or pincode-wise transaction data.
    Connects to a PostgreSQL database, executes a dynamic query, and displays a bar chart.
    """

    # --- Database Configuration ---
    DB_CONFIG = {
        "host": "your_host",
        "port": "your_port",
        "dbname": "your_dbname",
        "user": "your_username",
        "password": "your_password"
    }

    # --- Streamlit UI ---
    st.title("District-wise Transaction Analysis")

    # Sidebar inputs
    table = st.sidebar.text_input("Enter Table Name", value="your_table_name")
    pin_district = st.sidebar.selectbox("Group By Column", ["District_Name", "Pincode"])
    high_low = st.sidebar.selectbox("Sort Order", ["DESC", "ASC"])
    limit = st.sidebar.slider("Number of Top Records", min_value=5, max_value=50, value=10)
    metric = st.radio("Select Metric to Visualize", ["Amount", "Transactions"])

    # SQL query
    query = f"""
        SELECT
            "State",
            "{pin_district}" AS Group_Column,
            SUM("Transacion_count") AS total_transactions,
            SUM("Transacion_amount") AS total_amount
        FROM
            {table}
        GROUP BY
            "State", "{pin_district}"
        ORDER BY
            total_amount {high_low}, total_transactions {high_low}
        LIMIT {limit};
    """

    # Database connection
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        df = pd.read_sql_query(query, connection)
    except Exception as e:
        st.error(f"Database error: {e}")
        df = pd.DataFrame()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    # Visualization
    if not df.empty:
        if metric == "Amount":
            fig = px.bar(df, x="State", y="total_amount", color="Group_Column", text="Group_Column",
                         title=f"Total Transaction Amount by {pin_district}")
        else:
            fig = px.bar(df, x="State", y="total_transactions", color="Group_Column", text="Group_Column",
                         title=f"Total Transaction Count by {pin_district}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available to display.")
