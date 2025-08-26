import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

def visualize_transaction_summary():
    """
    Streamlit app to visualize transaction summary data from a PostgreSQL database.
    Displays a line chart showing transaction amount trends across states and transaction types.
    """

    # --- Streamlit UI ---
    st.title("Transaction Summary Visualization")

    # --- Database Configuration ---
    DB_CONFIG = {
        'host': 'your_host',         # e.g., 'localhost' or IP address
        'port': 'your_port',         # e.g., '5432'
        'dbname': 'your_database',   # e.g., 'transactions_db'
        'user': 'your_username',     # e.g., 'admin'
        'password': 'your_password'  # e.g., 'securepassword'
    }

    # --- SQL Query ---
    query = """
    SELECT
        "State",
        "Year",
        "Quarter",
        "Transaction_type",
        "Transaction_count",
        "Transaction_amount"
    FROM
        transaction_summary
    ORDER BY
        "State",
        "Year",
        "Quarter",
        "Transaction_type";
    """

    # --- Data Fetch and Visualization ---
    if st.button("Fetch and Visualize Data"):
        connection = None

        try:
            # Connect to the PostgreSQL database
            connection = psycopg2.connect(**DB_CONFIG)

            # Execute query and load results into a DataFrame
            df = pd.read_sql_query(query, connection)

            # Display the raw data
            st.subheader("Transaction Summary Data")
            st.dataframe(df)

            # Create an interactive line plot using Plotly Express
            fig = px.line(
                df,
                x="Quarter",
                y="Transaction_amount",
                color="State",
                line_group="Transaction_type",
                facet_col="Transaction_type",
                markers=True,
                title="Transaction Amount Trends Across States and Transaction Types",
                color_discrete_sequence=px.colors.qualitative.Set1
            )

            # Show the plot
            st.plotly_chart(fig)

        except Exception as e:
            # Display error message if something goes wrong
            st.error(f"Error: {e}")

        finally:
            # Clean up database resources
            if connection:
                connection.close()
