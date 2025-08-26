import streamlit as st

# Import visualization functions from respective modules
from district_analysis import visualize_district_transactions
from insurance_app import visualize_insurance_data
from transaction_metrics_app import visualize_transaction_metrics
from transaction_trends_visualization import visualize_transaction_summary
from user_distribution_app import visualize_user_distribution

# Set up the Streamlit page
st.set_page_config(page_title="Main Dashboard", layout="wide")
st.title("📊 Transaction Analytics Dashboard")

# Sidebar menu
st.sidebar.header("Select Visualization")
option = st.sidebar.radio(
    "Choose an analysis to display:",
    [
        "District-wise Transaction Analysis",
        "Insurance Transactions by State",
        "Transaction Metrics Over Time",
        "Transaction Trends Visualization",
        "User Registration Distribution"
    ]
)

# Conditional rendering based on user selection
if option == "District-wise Transaction Analysis":
    visualize_district_transactions()
elif option == "Insurance Transactions by State":
    visualize_insurance_data()
elif option == "Transaction Metrics Over Time":
    visualize_transaction_metrics()
elif option == "Transaction Trends Visualization":
    visualize_transaction_summary()
elif option == "User Registration Distribution":
    visualize_user_distribution()
