import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import Database as db

def visualize_transaction_metrics():
    """
    Streamlit app to visualize transaction metrics including:
    - Total transaction amount
    - Total transaction count
    - Average transaction value
    Grouped by state and quarter.
    """

    # --- Streamlit UI ---
    st.title("Transaction Metrics Over Time")

    # --- Database Configuration ---
    DB_CONFIG = {
        "host": db.db_host,
        "port": db.db_port,
        "dbname": db.db_name,
        "user": db.db_user,
        "password": db.db_password
    }

    # --- SQL Query ---
    query = """
    SELECT
        "State",
        "Year",
        "Quarter",
        SUM("Transaction_count") AS total_transactions,
        SUM("Transaction_amount") AS total_amount,
        ROUND(AVG("Transaction_amount" / NULLIF("Transaction_count", 0))::numeric, 2) AS avg_transaction_value
    FROM
        transaction_summary
    GROUP BY
        "State", "Year", "Quarter"
    ORDER BY
        "State", "Year", "Quarter";
    """

    # --- Data Fetch and Visualization ---
    if st.button("Fetch and Visualize Metrics"):
        connection = None
        cursor = None

        try:
            # Connect to the PostgreSQL database
            connection = psycopg2.connect(**DB_CONFIG)
            cursor = connection.cursor()

            # Execute query and load results into a DataFrame
            df = pd.read_sql_query(query, connection)

            # Display the raw data
            st.subheader("Transaction Metrics Summary")
            # st.dataframe(df)

            # Create a time column for plotting
            df["Time"] = df["Year"].astype(str) + "-" + df["Quarter"].astype(str)
            df.sort_values(by=["State", "Time"], inplace=True)

            # Melt the DataFrame for line plotting
            df_melted = df.melt(
                id_vars=["State", "Time"],
                value_vars=["total_amount", "total_transactions"],
                var_name="Metric",
                value_name="Value"
            )

            # Create line plot
            fig = px.line(
                df_melted,
                x="Time",
                y="Value",
                color="State",
                line_dash="Metric",
                title="Line Chart of Total Amount and Transactions by Quarter and State",
                labels={"Value": "Value", "Time": "Quarter"}
            )

            # Show the plot
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
