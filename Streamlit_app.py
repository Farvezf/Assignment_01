import streamlit as st
import pandas as pd
import pymysql

# SQL Connection
mydb = pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="Farvez@12345",
    database="red_bus_project"
)
mycursor = mydb.cursor()

st.title("Bus Details")

# Route Name Dropdown
mycursor.execute("SELECT DISTINCT route_name FROM Red_Bus_Data")
route_names = mycursor.fetchall()
route_name = st.sidebar.selectbox("Route", ["All"] + [item[0] for item in route_names])

# Dynamically update bustype and duration based on selected route
if route_name != "All":
    mycursor.execute(f"SELECT DISTINCT bustype FROM Red_Bus_Data WHERE route_name = '{route_name}'")
    bustypes = mycursor.fetchall()
else:
    mycursor.execute("SELECT DISTINCT bustype FROM Red_Bus_Data")
    bustypes = mycursor.fetchall()

bustype = st.sidebar.selectbox("Bus Type", ["All"] + [item[0] for item in bustypes])

if route_name != "All" and bustype != "All":
    mycursor.execute(f"SELECT DISTINCT duration FROM Red_Bus_Data WHERE route_name = '{route_name}' AND bustype = '{bustype}'")
    durations = mycursor.fetchall()
else:
    mycursor.execute("SELECT DISTINCT duration FROM Red_Bus_Data")
    durations = mycursor.fetchall()

# Duration Dropdown
duration = st.sidebar.selectbox("Duration", ["All"] + [item[0] for item in durations])

# Star Rating in slider format
star_rating = st.sidebar.slider(
    "Star Rating",
    1, 5, (1, 5)
)

# Price Range slider
price_range = st.sidebar.slider("Price Range", 0, 2000, (0, 2000))

# Seat Availability slider
seats_available = st.sidebar.slider("Seat Availability", 0, 100, (0, 100))

# Apply Filters button
if st.sidebar.button("Apply Filters"):
    query = "SELECT * FROM Red_Bus_Data WHERE "
    conditions = []

    if bustype != "All":
        conditions.append(f"bustype = '{bustype}'")
    if route_name != "All":
        conditions.append(f"route_name = '{route_name}'")
    if duration != "All":
        conditions.append(f"duration = '{duration}'")
    
    # Handling star rating filter based on slider selection
    if star_rating != (1, 5):
        conditions.append(f"star_rating BETWEEN {star_rating[0]} AND {star_rating[1]}")

    if price_range != (0, 2000):
        conditions.append(f"price BETWEEN {price_range[0]} AND {price_range[1]}")
    if seats_available != (0, 100):
        conditions.append(f"seats_available BETWEEN {seats_available[0]} AND {seats_available[1]}")

    if conditions:
        query += " AND ".join(conditions)
    else:
        query = "SELECT * FROM Red_Bus_Data"

    mycursor.execute(query)
    rows = mycursor.fetchall()

    df = pd.DataFrame(rows, columns=[
        'index', 'route_name', 'route_link', 'busname', 'bustype', 'departing_time', 
        'duration', 'reaching_time', 'star_rating', 'price', 'seats_available'
    ])

    # Select only the columns to display
    df = df[['route_name', 'route_link', 'busname', 'bustype', 'departing_time', 
             'duration', 'reaching_time', 'star_rating', 'price', 'seats_available']]

    if not rows:
        st.error("No buses found for the given input!")
    else:
        st.success("Data fetched successfully!")
        st.dataframe(df)