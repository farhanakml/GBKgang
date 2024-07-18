import pandas as pd
import altair as alt
import streamlit as st
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Dashboard E-Booking GBK",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

# Load data
df = pd.read_excel("Data E-booking GBK.xlsx")
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def make_donut(input_response, input_text, input_color):
    chart_color = {
        'green': ['#27AE60', '#12783D'],
        'red': ['#E74C3C', '#781F16']
    }.get(input_color, ['#29b5e8', '#155F7A'])
    
    source = pd.DataFrame({
        "Topic": [input_text, ''],
        "Value": [input_response, 100-input_response]
    })
    
    plot = alt.Chart(source).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color(field="Topic", type="nominal", scale=alt.Scale(range=chart_color), legend=None)
    ).properties(width=150, height=150)
    
    text = alt.Chart(pd.DataFrame({'text': [f'{input_response:.2f}%']})).mark_text(
        align='center', 
        fontSize=20, 
        fontWeight=600
    ).encode(
        text='text:N',
        x=alt.value(75),
        y=alt.value(75)
    )
    
    return plot + text

# Sidebar
with st.sidebar:
    st.image("gbklogo.png")
    month = st.selectbox(
        "Month :",
        ('All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    )
    st.write("You selected:", month)
    
    venues = {
        "Select": {"":""},
        "Lapangan Basket Indoor (GBK Arena)": {
            "Weekday": "Rp600.000\n - Session 10:00 - 12:00\n - Session 12:00 - 14:00\n - Session 14:00 - 16:00\n \n Rp800.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n \n Rp1.500.000\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00 ",
            "Weekend": "Rp1.500.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n - Session 10:00 - 12:00\n- Session 12:00 - 14:00\n - Session 14:00 - 16:00\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00"
        },
        "Lapangan Bulu Tangkis (GBK Arena)": {
            "Weekday": "Rp350.000\n - Session 10:00 - 12:00\n - Session 12:00 - 14:00\n - Session 14:00 - 16:00\n \n Rp400.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n \n Rp500.000\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00 ",
            "Weekend": "Rp500.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n - Session 10:00 - 12:00\n- Session 12:00 - 14:00\n - Session 14:00 - 16:00\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00"
        },
        "Lapangan Tenis Meja (GBK Arena)": {
            "Weekday": "Rp150.000\n - Session 10:00 - 12:00\n - Session 12:00 - 14:00\n - Session 14:00 - 16:00\n \n Rp400.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n \n Rp500.000\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00 ",
            "Weekend": "Rp500.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n - Session 10:00 - 12:00\n- Session 12:00 - 14:00\n - Session 14:00 - 16:00\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00"
        }
    }

    st.header("Price Check")
    selected_venue = st.selectbox("Select Venue", list(venues.keys()))
    selected_session = st.selectbox("Select Session", list(venues[selected_venue].keys()))
    price = venues[selected_venue][selected_session]
    st.write(f"{price}")

st.header("Hasil Analisa Data E-Booking Venue GBK Tahun 2023 :sparkles:")

# Dashboard Main Panel
col1, col2, col3 = st.columns((1, 4, 1), gap='medium')

with col1:
    st.markdown('#### Gains/Losses')

    if month == "All":
        visitor = df['Estimated Visitors'].sum()
        order = df['Type Date'].count()
        total_income = df['Price'].sum() / 1000000000
        income = '{0:.2f}'.format(total_income)

        st.metric('Total Estimated Visitors', value=visitor)
        st.metric('Total Order', value=order)
        st.metric('Total Income', value="Rp" + income + "M")
    
    else:
        df_month = df[df['Month'] == month]
        prev_month = month_order.index(month) - 1
        df_prev_month = df[df['Month'] == month_order[prev_month]]

        if month == "January":
            visitor = df_month['Estimated Visitors'].sum()
            order = df_month['Type Date'].count()
            total_income = df_month['Price'].sum() / 1000000
            income = '{0:.2f}'.format(total_income)

            st.metric('Total Estimated Visitors', value=visitor, delta=int(visitor), delta_color="off")
            st.metric('Total Order', value=order, delta=int(order), delta_color="off")
            st.metric('Total Income', value="Rp" + income + "Jt", delta="0%", delta_color="off")
        
        else:
            prev_visitor = df_prev_month['Estimated Visitors'].sum()
            visitor = df_month['Estimated Visitors'].sum()
            delta_visitor = int(visitor - prev_visitor)

            prev_order = df_prev_month['Type Date'].count()
            order = df_month['Type Date'].count()
            delta_order = int(order - prev_order)

            prev_total_income = df_prev_month['Price'].sum() / 1000000
            total_income = df_month['Price'].sum() / 1000000
            income = '{0:.2f}'.format(total_income)
            delta_income_percentage = '{0:.2%}'.format((total_income - prev_total_income) / prev_total_income)

            st.metric('Total Estimated Visitors', value=visitor, delta=delta_visitor)
            st.metric('Total Order', value=order, delta=delta_order)
            st.metric('Total Income', value="Rp" + income + "Jt", delta=delta_income_percentage)

    st.markdown('#### Booking Status')

    if month == "All":
        # Booked donut chart
        st.write("**Booked**")
        b = df[df['Status Order'] == 'Booked'].value_counts().sum() / df['Status Order'].value_counts().sum() * 100
        donut_chart_booked = make_donut(round(b, 2), 'Booked', 'green')
        st.altair_chart(donut_chart_booked, use_container_width=True)

        # Canceled donut chart
        st.write("**Canceled**")
        c = df[df['Status Order'] == 'Canceled'].value_counts().sum() / df['Status Order'].value_counts().sum() * 100
        donut_chart_canceled = make_donut(round(c, 2), 'Canceled', 'red')
        st.altair_chart(donut_chart_canceled, use_container_width=True)
    
    else:
        # Booked donut chart
        st.write("**Booked**")
        b = df_month[df_month['Status Order'] == 'Booked'].value_counts().sum() / df_month['Status Order'].value_counts().sum() * 100
        donut_chart_booked = make_donut(round(b, 2), 'Booked', 'green')
        st.altair_chart(donut_chart_booked, use_container_width=True)

        # Canceled donut chart
        st.write("**Canceled**")
        c = df_month[df_month['Status Order'] == 'Canceled'].value_counts().sum() / df_month['Status Order'].value_counts().sum() * 100
        donut_chart_canceled = make_donut(round(c, 2), 'Canceled', 'red')
        st.altair_chart(donut_chart_canceled, use_container_width=True)

with col2:
    st.markdown('#### Total Orders by Month')
    order_counts = df.groupby('Month')['Status Order'].count().reset_index()
    order_chart = alt.Chart(order_counts).mark_bar().encode(
        x=alt.X('Month', sort=month_order, title='Month'),
        y=alt.Y('Status Order', title='Total Order'),
        tooltip=['Month', 'Status Order']
    ).properties(
        width='container',  # Adjusted width
        height=300   # Adjusted height
    )
    st.altair_chart(order_chart, use_container_width=True)

    st.markdown('#### Number of Bookings per Venue')
    venue_order_counts = df['Venue Name'].value_counts().reset_index()
    venue_order_counts.columns = ['Venue Name', 'Count']
    venue_chart = alt.Chart(venue_order_counts).mark_bar().encode(
        x=alt.X('Count:Q', title='Number of Bookings'),
        y=alt.Y('Venue Name:N', sort='-x', title='Venue Name'),
        tooltip=['Venue Name', 'Count']
    ).properties(
        width='container',  # Adjusted width
        height=450,
        background='rgba(0, 0, 0, 0)',  # Set background to transparent
        padding={'left': 5, 'top': 5, 'right': 5, 'bottom': 5}
    ).configure_view(
        strokeOpacity=0  # Remove chart borders to make the background fully transparent
    )
    st.altair_chart(venue_chart, use_container_width=True)

    st.markdown('#### Number of Bookings per Session Time')
    session_order_counts = df['Session Time'].value_counts().reset_index()
    session_order_counts.columns = ['Session Time', 'Count']
    session_chart = alt.Chart(session_order_counts).mark_bar().encode(
        x=alt.X('Count:Q', title='Number of Bookings'),
        y=alt.Y('Session Time:N', sort='-x', title='Session Time'),
        tooltip=['Session Time', 'Count']
    ).properties(
        width='container',  # Adjusted width
        height=450,
        background='rgba(0, 0, 0, 0)',  # Set background to transparent
        padding={'left': 5, 'top': 5, 'right': 5, 'bottom': 5}
    ).configure_view(
        strokeOpacity=0  # Remove chart borders to make the background fully transparent
    )
    st.altair_chart(session_chart, use_container_width=True)

with col3:

    with st.expander('About', expanded=True):
        st.write('''
            - Data: [GBK E-Booking](https://example.com).
            - :green[**Gains/Losses**]: Metrics for total estimated visitors, total orders, and total income.
            - :green[**Booking Status**]: Percentage of bookings categorized as booked or canceled.
            - :green[**Total Orders by Month**]: Number of orders per month.
            - :green[**Number of Bookings per Venue**]: Number of bookings for each venue.
            - :green[**Number of Bookings per Session Time**]: Number of bookings for each session time.
        ''')
