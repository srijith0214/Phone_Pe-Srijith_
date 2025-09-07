# district_visualization.py

import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import Database as db

def visualize_district_transactions():
    """
    Streamlit app to visualize district-wise or pincode-wise transaction data.
    Connects to a PostgreSQL database, executes a dynamic query, and displays a bar chart.
    """

    # --- Database Configuration ---
    DB_CONFIG = {
        "host": db.db_host,
        "port": db.db_port,
        "dbname": db.db_name,
        "user": db.db_user,
        "password": db.db_password
    }

    # --- Streamlit UI ---
    st.title("District-wise Transaction Analysis")

    # Sidebar inputs
    table = st.sidebar.radio("Enter Table Name",["top_transaction_summary_pin","top_transaction_summary"])
    pin_district = st.sidebar.selectbox("Group By Column", ["Pincode","District_Name"])
    high_low = st.sidebar.selectbox("Sort Order", ["DESC", "ASC"])
    limit = st.sidebar.slider("Number of Top Records", min_value=5, max_value=50, value=10)
    metric = st.radio("Select Metric to Visualize", ["Amount", "Transactions"])

    # SQL query
    query = f"""
        SELECT
            "State",
            "{pin_district}" AS "{pin_district}",
            SUM("Transaction_count") AS total_transactions,
            SUM("Transaction_amount") AS total_amount
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
        print(df)
    except Exception as e:
        st.error(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    # Visualization
    if not df.empty:
        if metric == "Amount":
            fig = px.bar(df, x="State", y="total_amount", color=f"{pin_district}", text=f"{pin_district}",
                         title=f"Total Transaction Amount by {pin_district}")
        else:
            fig = px.bar(df, x="State", y="total_transactions", color=f"{pin_district}", text=f"{pin_district}",
                         title=f"Total Transaction Count by {pin_district}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available to display.")
