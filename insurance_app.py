import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import Database as db
def visualize_insurance_data():
    """
    Streamlit app function to visualize PhonePe insurance transactions by state.
    Connects to a PostgreSQL database, executes a query on the insurance_summary table,
    and displays the results using a scatter plot with log-scaled x-axis.
    """

    # Title of the app
    st.title("PhonePe Insurance Transactions by State")

    # --- Database Configuration ---
    # Replace these values with your actual database credentials
    DB_CONFIG = {
        "host": db.db_host,
        "port": db.db_port,
        "dbname": db.db_name,
        "user": db.db_user,
        "password": db.db_password
    }


    # --- Sidebar Inputs ---
    # Allow user to customize query parameters
    st.sidebar.header("Query Parameters")
    high_low = st.sidebar.selectbox("Sort Order", options=["DESC", "ASC"], index=0)
    limit = st.sidebar.slider("Limit Results", min_value=5, max_value=50, value=20)

    # --- SQL Query ---
    # Dynamically formatted query based on user input
    query = f"""
      SELECT
        "State",
        SUM("Transaction_count") AS total_transactions,
        SUM("Transaction_amount") AS total_amount
      FROM
        insurance_summary
      GROUP BY
        "State"
      ORDER BY
        total_amount {high_low}, total_transactions {high_low}
      LIMIT {limit};
    """

    # --- Data Fetch and Visualization ---
    if st.button("Fetch and Visualize Data"):
        connection = None
        cursor = None

        try:
            # Connect to the PostgreSQL database
            connection = psycopg2.connect(**DB_CONFIG)
            cursor = connection.cursor()

            # Execute query and load results into a DataFrame
            df = pd.read_sql_query(query, connection)

            # Display the raw data
            st.subheader("Insurance Summary by State")
            # st.dataframe(df)

            # Create a scatter plot with log-scaled x-axis
            fig = px.scatter(
                df,
                x="total_transactions",
                y="total_amount",
                size="total_amount",
                color="State",
                hover_name="State",
                hover_data={"total_transactions": True},
                size_max=45,
                title="PhonePe Insurance Transactions by State",
                log_x=True  # Log scale for better visualization
            )

            # Show the plot
            st.plotly_chart(fig)

        except Exception as e:
            # Display error message if something goes wrong
            st.error(f"Error: {e}")

        finally:
            # Clean up database resources
            if cursor:
                cursor.close()
            if connection:
                connection.close()
