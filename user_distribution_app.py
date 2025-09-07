import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import Database as db

def visualize_user_distribution():
    """
    Streamlit app to visualize user registration data by State or District.
    Displays a choropleth map for states or a histogram for districts.
    """

    # --- Streamlit UI ---
    st.title("User Registration Distribution")

    # --- Database Configuration ---
    DB_CONFIG = {
        "host": db.db_host,
        "port": db.db_port,
        "dbname": db.db_name,
        "user": db.db_user,
        "password": db.db_password
    }


    # --- Sidebar Inputs ---
    st.sidebar.header("Query Parameters")
    plot_level = st.sidebar.selectbox("Select Plot Level", ["State", "District"])
    high_low = st.sidebar.selectbox("Sort Order (District Only)", ["DESC", "ASC"])
    limit = st.sidebar.slider("Limit Records (District Only)", min_value=5, max_value=50, value=20)

    # --- SQL Query Construction ---
    if plot_level == 'State':
        query = f"""
        SELECT "State", SUM("registeredUsers") AS total_users
        FROM user_summary
        GROUP BY "State"
        ORDER BY total_users;
        """
    else:
        query = f"""
        SELECT "State", "District_Name", SUM("registeredUsers") AS total_users
        FROM user_summary
        GROUP BY "State", "District_Name"
        ORDER BY total_users {high_low}
        LIMIT {limit};
        """

    # --- Database Connection and Query Execution ---
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        df = pd.read_sql_query(query, connection)
    except Exception as e:
        st.error(f"Database error: {e}")
        return
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    # --- Visualization ---
    if plot_level == 'State':
        # State name mapping for geojson compatibility
        state_mapping = {
            'arunachal-pradesh': 'Arunanchal Pradesh',
            'andhra-pradesh': 'Andhra Pradesh',
            'assam': 'Assam',
            'bihar': 'Bihar',
            'chhattisgarh': 'Chhattisgarh',
            'goa': 'Goa',
            'gujarat': 'Gujarat',
            'haryana': 'Haryana',
            'himachal-pradesh': 'Himachal Pradesh',
            'jharkhand': 'Jharkhand',
            'karnataka': 'Karnataka',
            'kerala': 'Kerala',
            'madhya-pradesh': 'Madhya Pradesh',
            'maharashtra': 'Maharashtra',
            'manipur': 'Manipur',
            'meghalaya': 'Meghalaya',
            'mizoram': 'Mizoram',
            'nagaland': 'Nagaland',
            'odisha': 'Odisha',
            'puducherry': 'Puducherry',
            'punjab': 'Punjab',
            'rajasthan': 'Rajasthan',
            'sikkim': 'Sikkim',
            'tamil-nadu': 'Tamil Nadu',
            'telangana': 'Telangana',
            'tripura': 'Tripura',
            'uttar-pradesh': 'Uttar Pradesh',
            'west-bengal': 'West Bengal',
            'andaman-&-nicobar-islands': 'Andaman & Nicobar',
            'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
            'delhi': 'Delhi',
            'lakshadweep': 'Lakshadweep',
            'jammu-&-kashmir': 'Jammu & Kashmir',
            'ladakh': 'Ladakh'
        }
        df['State'] = df['State'].replace(state_mapping)
        print(df['State'])
        # Choropleth map
        fig = px.choropleth(
            df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='total_users',
            color_continuous_scale='Reds',
            title="Total Registered Users by State"
        )
        fig.update_geos(fitbounds="locations", visible=False)
    else:
        # Histogram for district-level data
        fig = px.histogram(
            df,
            x='State',
            y='total_users',
            nbins=2,
            color='District_Name',
            title='Total Registered Users by District'
        )

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)
