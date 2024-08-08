import pandas as pd
import altair as alt
import streamlit as st
import plotly.express as px
import holidays
from datetime import datetime
import calendar as cal

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


def make_donut(booked, canceled, input_color):
    if input_color == 'green':
        chart_color = ['#27AE60', '#E74C3C']

    total = booked + canceled
    booked_percentage = booked / total * 100
    canceled_percentage = canceled / total * 100

    source = pd.DataFrame({
        "Status": ["Booked", "Canceled"],
        "Value": [booked, canceled],
        "Percentage": [booked_percentage, canceled_percentage]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=70, outerRadius=85, cornerRadius=10).encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color("Status:N",
                        scale=alt.Scale(
                            domain=["Booked", "Canceled"],
                            range=chart_color),
                        legend=None),
        tooltip=[alt.Tooltip("Status:N"), alt.Tooltip("Value:Q"), alt.Tooltip("Percentage:Q", format=".1f")]
    ).properties(width=200, height=200)

    text = alt.Chart(pd.DataFrame({'text': [f'{booked_percentage:.1f}%']})).mark_text(
        align='center', fontSize=30, fontWeight=600, color='#27AE60'
    ).encode(
        text='text:N'
    ).properties(width=200, height=200)

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

    with st.expander("**Price Check**"):
        selected_venue = st.selectbox("Select Venue", list(venues.keys()))
        selected_session = st.selectbox("Select Session", list(venues[selected_venue].keys()))
        price = venues[selected_venue][selected_session]
        st.write(f"{price}")

st.header("Hasil Analisa Data E-Booking Venue GBK Tahun 2023 :sparkles:")

# Dashboard Main Panel
col1, col2 = st.columns((1.5, 5.5), gap='large')

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
        b=df[df['Status Order'] == 'Booked'].value_counts().sum()
        c=df[df['Status Order'] == 'Canceled'].value_counts().sum()
        donut_chart_greater = make_donut(round(b,2), round(c,2), 'green')
        st.altair_chart(donut_chart_greater, use_container_width=True)
    
    else:
        # Booked donut chart
        b=df_month[df_month['Status Order'] == 'Booked'].value_counts().sum()
        c=df_month[df_month['Status Order'] == 'Canceled'].value_counts().sum()
        donut_chart_greater = make_donut(round(b,2), round(c,2), 'green')
        st.altair_chart(donut_chart_greater, use_container_width=True)
    
    with st.expander('About', expanded=True):
            st.write('''
                - Data: [GBK E-Booking](https://example.com).
                - :green[**Gains/Losses**]: Metrics for total estimated visitors, total orders, and total income.
                - :green[**Booking Status**]: Percentage of bookings categorized as booked or canceled.
                - :green[**Total Orders by Month**]: Number of orders per month.
                - :green[**Number of Bookings per Venue**]: Number of bookings for each venue.
                - :green[**Number of Bookings per Session Time**]: Number of bookings for each session time.
            ''')


with col2:
    incol1, incol2 = st.columns((4, 1.5), gap='large')
    with incol1 :
        if month == "All":
            st.markdown('#### Total Orders by Month')
            order_counts = df.groupby('Month')['Status Order'].count().reset_index()
            order_chart = alt.Chart(order_counts).mark_bar(color='#30cb70').encode(
                x=alt.X('Month', sort=month_order, title='Month'),
                y=alt.Y('Status Order', title='Total Order'),
                tooltip=['Month', 'Status Order']
            ).properties(
                width='container',  # Adjusted width
                height=450   # Adjusted height
            )
            
            st.altair_chart(order_chart, use_container_width=True)

        else:
            st.markdown('#### Total Orders by Month')
            order_counts = df_month.groupby(df_month['Schedule Date'].dt.date).size().reset_index(name='Total Orders')
            start_date = df_month['Schedule Date'].min().replace(day=1)
            end_date = df_month['Schedule Date'].max().replace(day=1) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
            date_range = pd.date_range(start=start_date, end=end_date)

            chart = alt.Chart(order_counts).mark_bar(color='#30cb70').encode(
                x=alt.X('Schedule Date:T', title='Date', axis=alt.Axis(format='%d', labelAngle=-0)),
                y=alt.Y('Total Orders:Q', title='Total Orders'),
                tooltip=['Schedule Date:T', 'Total Orders:Q']
            ).properties(
                title='Total Orders per Date in ' + month,
                # width='container',
                height=450
            ).configure_axisX(
                labelAngle=-45,
                labelFontSize=10,
                tickCount=len(date_range),
                labelOverlap=False
            )
            st.altair_chart(chart,  use_container_width=True)

    with incol2:
        if month == "All":
            highest_month = df.groupby('Month').size().sort_values(ascending=False)
            first_month = highest_month.index[0]
            second_month = highest_month.index[1]
            last_month = highest_month.index[-1]
            highest_venue = df.groupby('Venue Name').size().sort_values(ascending=False)
            first_venue = highest_venue.index[0]
            second_venue = highest_venue.index[1]
            st.markdown(f"**Peak Booking Times:** Most bookings occur in {first_month} and {second_month}.")
            st.markdown(f"**Popular Venues:** {first_venue} and {second_venue} have the highest booking rates.")
            st.markdown(f"**Recommendations:** Consider increasing marketing efforts in {last_month} due to historically low bookings.")
        else:
            df_month = df[df['Month'] == month]
            highest_venue = df_month.groupby('Venue Name').size().sort_values(ascending=False)
            
            if not highest_venue.empty:
                first_venue = highest_venue.index[0]
                second_venue = highest_venue.index[1] if len(highest_venue) > 1 else None
                st.markdown(f"**Popular Venues:** {first_venue} and {second_venue} have the highest booking rates.")
            else:
                st.markdown("No bookings found for the selected month.")
            
            total_orders = df_month['Venue Name'].count()
            st.markdown(f"**Total Orders in {month}:** {total_orders}")

            highest_day = df_month.groupby(df_month['Schedule Date'].dt.date).size().sort_values(ascending=False)
            if not highest_day.empty:
                highest_booking_day = highest_day.index[0]
                highest_booking_count = highest_day.iloc[0]
                st.markdown(f"**Highest Day Booking:** The highest number of bookings was on {highest_booking_day} with {highest_booking_count} bookings.")
            else:
                st.markdown("No booking days found for the selected month.")
                
            country = 'ID'
            year = 2023
            month_name = month
            month_number = list(cal.month_name).index(month_name)

            holiday_list = holidays.CountryHoliday(country, years=year)
            holiday_dates = {date: name for date, name in holiday_list.items()}
            filtered_holidays = {date: name for date, name in holiday_dates.items() if date.month == month_number}
            holiday_items = [f"{date.strftime('%d')} {month_name}: {name}" for date, name in filtered_holidays.items()]

            st.markdown(f"**Holidays in {month_name} :**")
            for holiday in holiday_items:
                st.write(holiday)


    if month == "All":
        st.markdown('#### Number of Bookings per Venue')
        venue_order_counts = df['Venue Name'].value_counts().reset_index()
        venue_order_counts.columns = ['Venue Name', 'Count']
        venue_chart = alt.Chart(venue_order_counts).mark_bar(color='#30cb70').encode(
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
    else:
        st.markdown('#### Number of Bookings per Venue')
        venue_order_counts = df_month['Venue Name'].value_counts().reset_index()
        venue_order_counts.columns = ['Venue Name', 'Count']
        venue_chart = alt.Chart(venue_order_counts).mark_bar(color='#30cb70').encode(
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

with col2:
    if month == "All":
        st.markdown('#### Number of Bookings per Session Time')
        session_order_counts = df['Session Time'].value_counts().reset_index()
        session_order_counts.columns = ['Session Time', 'Count']
        session_chart = alt.Chart(session_order_counts).mark_bar(color='#30cb70').encode(
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
    
    else:
        st.markdown('#### Number of Bookings per Session Time')
        session_order_counts = df_month['Session Time'].value_counts().reset_index()
        session_order_counts.columns = ['Session Time', 'Count']
        session_chart = alt.Chart(session_order_counts).mark_bar(color='#30cb70').encode(
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
