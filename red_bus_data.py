import streamlit as st
import pandas as pd
import pymysql

# SQL Connection
# Create a connection to the database
mydb = pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="Farvez@12345",
    database="red_bus_project"
)
mycursor = mydb.cursor()

st.title("Red Bus Data")

# Input fields in sidebar
mycursor.execute("SELECT DISTINCT route_name FROM Red_Bus_Data")
route_names = mycursor.fetchall()
route_name = st.sidebar.selectbox("Route Name", ["All"] + [item[0] for item in route_names])

mycursor.execute("SELECT DISTINCT busname FROM Red_Bus_Data")
busnames = mycursor.fetchall()
busname = st.sidebar.selectbox("Bus Name", ["All"] + [item[0] for item in busnames])

mycursor.execute("SELECT DISTINCT bustype FROM Red_Bus_Data")
bustypes = mycursor.fetchall()
bustype = st.sidebar.selectbox("Bus Type", ["All"] + [item[0] for item in bustypes])

mycursor.execute("SELECT DISTINCT departing_time FROM Red_Bus_Data")
departing_times = mycursor.fetchall()
departing_time = st.sidebar.selectbox("Departing Time", ["All"] + [item[0] for item in departing_times])

mycursor.execute("SELECT DISTINCT duration FROM Red_Bus_Data")
durations = mycursor.fetchall()
duration = st.sidebar.selectbox("Duration", ["All"] + [item[0] for item in durations])

mycursor.execute("SELECT DISTINCT reaching_time FROM Red_Bus_Data")
reaching_times = mycursor.fetchall()
reaching_time = st.sidebar.selectbox("Reaching Time", ["All"] + [item[0] for item in reaching_times])

mycursor.execute("SELECT DISTINCT star_rating FROM Red_Bus_Data")
star_ratings = mycursor.fetchall()
star_rating = st.sidebar.selectbox("Star Rating", ["All"] + [item[0] for item in star_ratings])

mycursor.execute("SELECT DISTINCT price FROM Red_Bus_Data")
prices = mycursor.fetchall()
price = st.sidebar.selectbox("Price", ["All"] + [item[0] for item in prices])

# Form submit button
submit_button = st.sidebar.button(label='Fetch Data')

# If the form is submitted
if submit_button:
    query = "SELECT * FROM Red_Bus_Data WHERE "
    conditions = []

    if route_name != "All":
        conditions.append(f"route_name = '{route_name}'")
    if busname != "All":
        conditions.append(f"busname = '{busname}'")
    if bustype != "All":
        conditions.append(f"bustype = '{bustype}'")
    if departing_time != "All":
        conditions.append(f"departing_time = '{departing_time}'")
    if duration != "All":
        conditions.append(f"duration = '{duration}'")
    if reaching_time != "All":
        conditions.append(f"reaching_time = '{reaching_time}'")
    if star_rating != "All":
        conditions.append(f"star_rating = '{star_rating}'")
    if price != "All":
        conditions.append(f"price = '{price}'")

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
    
    df['price'] = df['price'].apply(lambda x: round(x, 2))
    df['star_rating'] = df['star_rating'].apply(lambda x: round(x, 1))
    df = df.drop(df.columns[0], axis=1)

    if not rows:
        st.error("No buses found for the given input!")
    else:
        st.success("Data fetched successfully!")
        st.write("Here are your details:")
        st.dataframe(df)