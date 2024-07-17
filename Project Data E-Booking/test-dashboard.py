# Mengimport library yang akan digunakan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Dashboard E-Booking GBK",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

# Mengread dataset dari file hasil pemrosesan
df = pd.read_excel("Data E-booking GBK.xlsx")
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def make_donut(input_response, input_text, input_color):
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=25, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

with st.sidebar:
    # logo untuk sidebar
    st.image("gbklogo.png")

    month = st.selectbox(
    "Month :",
    ('All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'))
    
    st.write("You selected:", month)
    
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

# Membuat judul dashboard
st.header("Hasil Analisa Data E-Booking Venue GBK Tahun 2023 :sparkles:")

col1, col2, col3 = st.columns(3)

if month == "All": 
    with col1:
        tile = col1.container(
            height=105)
        visitor = df['Estimated Visitors'].sum()
        tile.metric('Total Estimated Visitors', value = visitor)
        
    with col2:
        tile = col2.container(
            height=105)
        order = df['Type Date'].count()
        tile.metric('Total Order', value = order)

    with col3:
        tile = col3.container(
            height=105)
        total_permiliar = df['Price'].sum() / 1000000000
        income = '{0:.2f}'.format(total_permiliar)
        tile.metric('Total Income', value = "Rp" + income + "M")
    
    #Orders by Month
    order_counts = df.groupby('Month')['Status Order'].count().reset_index()

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
        # st.markdown("**Ratio of Order Distribution**")
        # fig, ax = plt.subplots(figsize=(8, 6))
        # ax.pie(df['Status Order'].value_counts(), labels=df['Status Order'].value_counts().index, autopct='%1.1f%%', startangle=140, colors=['#4169e1','#dc143c'])
        # ax.set_title('Status Order Distribution')
        # st.pyplot(fig)

        st.write("**Booked**")
        b=df[df['Status Order'] == 'Booked'].value_counts().sum()/df['Status Order'].value_counts().sum()*100
        donut_chart_greater = make_donut(round(b,2), 'Inbound Migration', 'green')
        st.altair_chart(donut_chart_greater)

        st.write("**Canceled**")
        c=df[df['Status Order'] == 'Canceled'].value_counts().sum()/df['Status Order'].value_counts().sum()*100
        donut_chart_greater = make_donut(round(c,2), 'Inbound Migration', 'red')
        st.altair_chart(donut_chart_greater)


    with col2:
        st.markdown("**Relation Between Session Time and Order Count**")
        fig, ax = plt.subplots(figsize=(6, 6))
        sns.barplot(x=df['Session Time'].value_counts(), y=df['Session Time'].value_counts().index, palette='Blues_r', ax=ax)
        ax.set_title('Number of Bookings per Session Time')
        ax.set_xlabel('Number of Bookings')
        ax.set_ylabel('Session Time')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    st.markdown("**Amount of Vanue Order**")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=df['Venue Name'].value_counts(), y=df['Venue Name'].value_counts().index, palette='Blues_r')
    ax.set_title('Number of Bookings per Venue')
    ax.set_xlabel('Number of Bookings')
    ax.set_ylabel('Venue Name')
    st.pyplot(fig)

if month != "All":
    df_month = df[df['Month'] == month]
    prev_month = month_order.index(month) - 1
    df_prev_month = df[df['Month'] == month_order[prev_month]]

    if month == "January":
        with col1:
            tile = col1.container(height=125)
            visitor = df_month['Estimated Visitors'].sum()
            tile.metric('Total Estimated Visitors', value = visitor, delta = visitor.item(), delta_color="off")
            
        with col2:
            tile = col2.container(height=125)
            order = df_month['Type Date'].count()
            tile.metric('Total Order', value = order, delta = order.item(), delta_color="off")

        with col3:
            tile = col3.container(height=125)
            total_perjuta = df_month['Price'].sum() / 1000000
            income = '{0:.2f}'.format(total_perjuta)
            tile.metric('Total Income', value = "Rp" + income + "Jt", delta = "0%", delta_color="off")
    else:
        with col1:
            tile = col1.container(height=125)
            prev_visitor = df_prev_month['Estimated Visitors'].sum()
            visitor = df_month['Estimated Visitors'].sum()
            delta_visitor = (visitor - prev_visitor).item()
            tile.metric('Total Estimated Visitors', value = visitor, delta = delta_visitor)
            
        with col2:
            tile = col2.container(height=125)
            prev_order = df_prev_month['Type Date'].count()
            order = df_month['Type Date'].count()
            delta_order = (order - prev_order).item()
            tile.metric('Total Order', value = order, delta = delta_order)

        with col3:
            tile = col3.container(height=125)
            prev_total_perjuta = df_prev_month['Price'].sum() / 1000000
            total_perjuta = df_month['Price'].sum() / 1000000
            income = '{0:.2f}'.format(total_perjuta)
            delta_income = total_perjuta - prev_total_perjuta
            delta_income_percentage = '{0:.2%}'.format((total_perjuta - prev_total_perjuta) / prev_total_perjuta)
            tile.metric('Total Income', value = "Rp" + income + "Jt", delta = delta_income_percentage)

    order_counts = df_month.groupby(df_month['Schedule Date'].dt.date).size().reset_index(name='Total Orders')

    start_date = df_month['Schedule Date'].min().replace(day=1)
    end_date = df_month['Schedule Date'].max().replace(day=1) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
    date_range = pd.date_range(start=start_date, end=end_date)
    # Create the chart
    chart = alt.Chart(order_counts).mark_bar().encode(
        x=alt.X('Schedule Date:T', title='Date', axis=alt.Axis(format='%d', labelAngle=-0)),
        y=alt.Y('Total Orders:Q', title='Total Orders'),
        tooltip=['Schedule Date:T', 'Total Orders:Q']
    ).properties(
        title='Total Orders per Date in ' + month,
        width=700,
        height=400
    ).configure_axisX(
        labelAngle=-45,
        labelFontSize=10,
        tickCount=len(date_range),
        labelOverlap=False
    )
    
    # Display the chart in Streamlit
    st.altair_chart(chart)
    
    # Orders by Month
    
    # order_counts = df.groupby(['Month', 'Date'])['Status Order'].count().reset_index()
    # month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # chart = alt.Chart(order_counts).mark_bar().encode(
    #     x=alt.X('Date', bin=alt.Bin(maxbins=31)),
    #     y=alt.Y('Status Order', title='Total Order'),
    #     tooltip=['Date', 'Status Order']
    # ).properties(
    #     title='Total Orders by Date',
    #     width=800,
    #     height=450)
    # st.altair_chart(chart)

    col1, col2 = st.columns(2)
    with col1:
        # st.markdown("**Ratio of Order Distribution**")
        # fig, ax = plt.subplots(figsize=(8, 6))
        # ax.pie(df_month['Status Order'].value_counts(), labels=df_month['Status Order'].value_counts().index, autopct='%1.1f%%', startangle=140, colors=['#4169e1','#dc143c'])
        # ax.set_title('Status Order Distribution')
        # st.pyplot(fig)

        st.write("**Booked**")
        b=df_month[df_month['Status Order'] == 'Booked'].value_counts().sum()/df_month['Status Order'].value_counts().sum()*100
        donut_chart_greater = make_donut(round(b,2), 'Success Transaction', 'green')
        st.altair_chart(donut_chart_greater)

        st.write("**Canceled**")
        c=df_month[df_month['Status Order'] == 'Canceled'].value_counts().sum()/df_month['Status Order'].value_counts().sum()*100
        donut_chart_greater = make_donut(round(c,2), 'Canceled Transaction', 'red')
        st.altair_chart(donut_chart_greater)

    with col2:
        st.markdown("**Relation Between Session Time and Order Count**")
        fig, ax = plt.subplots(figsize=(6, 6))
        sns.barplot(x=df_month['Session Time'].value_counts(), y=df_month['Session Time'].value_counts().index, palette='Blues_r', ax=ax)
        ax.set_title('Number of Bookings per Session Time')
        ax.set_xlabel('Number of Bookings')
        ax.set_ylabel('Session Time')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    
