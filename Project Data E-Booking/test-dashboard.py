# Mengimport library yang akan digunakan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt

# Mengread dataset dari file hasil pemrosesan
df = pd.read_excel("Data E-booking GBK.xlsx")







with st.sidebar:
    # logo untuk sidebar
    st.image("gbklogo.png")

    bulan = st.selectbox(
    "Month :",
    ('All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'))
    
    st.write("You selected:", bulan)
    
    venues = {
    "Select" : {"":""},
    "Lapangan Basket Indoor (GBK Arena)": {"Weekday": "Rp600.000\n - Session 10:00 - 12:00\n - Session 12:00 - 14:00\n - Session 14:00 - 16:00\n \n Rp800.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n \n Rp1.500.000\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00 ",
                                           "Weekend": "Rp1.500.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n - Session 10:00 - 12:00\n- Session 12:00 - 14:00\n - Session 14:00 - 16:00\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00"},
    "Lapangan Bulu Tangkis (GBK Arena)": {"Weekday": "Rp350.000\n - Session 10:00 - 12:00\n - Session 12:00 - 14:00\n - Session 14:00 - 16:00\n \n Rp400.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n \n Rp500.000\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00 ",
                                           "Weekend": "Rp500.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n - Session 10:00 - 12:00\n- Session 12:00 - 14:00\n - Session 14:00 - 16:00\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00"},
    "Lapangan Tenis Meja (GBK Arena)": {"Weekday": "Rp150.000\n - Session 10:00 - 12:00\n - Session 12:00 - 14:00\n - Session 14:00 - 16:00\n \n Rp400.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n \n Rp500.000\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00 ",
                                           "Weekend": "Rp500.000\n - Session 06:00 - 08:00\n - Session 08:00 - 10:00\n - Session 10:00 - 12:00\n- Session 12:00 - 14:00\n - Session 14:00 - 16:00\n - Session 16:00 - 18:00\n - Session 18:00 - 20:00\n - Session 20:00 - 22:00"},
}

    # Sidebar for venue selection
    st.header("Price Check")
    selected_venue = st.selectbox("Select Venue", list(venues.keys()))
    selected_session = st.selectbox("Select Session", list(venues[selected_venue].keys()))

    # Display the price for the selected venue and session
    price = venues[selected_venue][selected_session]
    st.write(f"{price}")
    
    
    
    
    # # Pembuatan Toggle untuk melihat dataset
    # toggle_dataset = st.toggle('Cek Dataset')



# Membuat judul dashboard
st.header("Hasil Analisa Data E-Booking Venue GBK Tahun 2023 :sparkles:")

col1, col2, col3 = st.columns(3)

if bulan == "All": 
    
    with col1:
        visitor = df['Estimated Visitors'].sum()
        st.metric('Total Estimated Visitors', value = visitor)
        
    with col2:
        order = df['Type Date'].count()
        st.metric('Total Order', value = order)

    with col3:
        total_permiliar = df['Price'].sum() / 1000000000
        income = '{0:.2f}'.format(total_permiliar)
        st.metric('Total Income', value = "Rp" + income + "M")

    #Orders by Month
    order_counts = df.groupby('Month')['Status Order'].count().reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    chart = alt.Chart(order_counts).mark_bar().encode(
        x=alt.X('Month', sort=month_order, title='Month'),
        y=alt.Y('Status Order', title='Total Order'),
        tooltip=['Month', 'Status Order']
    ).properties(
        title='Total Orders by Month',
        width=800,
        height=450)
    st.altair_chart(chart)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Ratio of Order Distribution**")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(df['Status Order'].value_counts(), labels=df['Status Order'].value_counts().index, autopct='%1.1f%%', startangle=140, colors=['#4169e1','#dc143c'])
        ax.set_title('Status Order Distribution')
        st.pyplot(fig)

    with col2:
        st.markdown("**Relation Between Session Time and Order Count**")
        fig, ax = plt.subplots(figsize=(6, 6))
        sns.barplot(x=df['Session Time'].value_counts(), y=df['Session Time'].value_counts().index, palette='Blues_r', ax=ax)
        ax.set_title('Number of Bookings per Session Time')
        ax.set_xlabel('Number of Bookings')
        ax.set_ylabel('Session Time')
        plt.xticks(rotation=45)
        st.pyplot(fig)



    
