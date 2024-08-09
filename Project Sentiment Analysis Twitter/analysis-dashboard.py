import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import altair as alt

# Membaca data dari file CSV
# Ubah 'data.csv' menjadi path file Anda
df = pd.read_excel('Hasil Sentiment Analysis GBK Juni 2024.xlsx')

# Convert 'created_at' ke datetime
df['created_at'] = pd.to_datetime(df['created_at'])

# Page configuration
st.set_page_config(
    page_title="Dashboard Sentiment Analysis GBK",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

col1, col2 = st.columns((6,4), gap = 'small')
with col1:
    st.title('Sentiment Analysis Dashboard for GBK')
with col2:
    month = st.selectbox("a", "b")
# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["All", "Positive 😊", "Negative ☹️", "Neutral 😐"])

col1, col2, col3 = st.columns((2,2,2), gap='large')



with col1:
    # Menampilkan WordCloud
    st.header('WordCloud')
    all_text = ' '.join(df['full_text'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(all_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

with col2:
    df['date'] = df['created_at'].dt.date
    tweet_per_day = df.groupby('date').size().reset_index(name='count')

    # Create the Altair chart
    chart = alt.Chart(tweet_per_day).mark_line(point=alt.OverlayMarkDef()).encode(
        x=alt.X('date:T', axis=alt.Axis(title='Date')),
        y=alt.Y('count:Q', axis=alt.Axis(title='Number of Tweets')),
        tooltip=['date', 'count']
    ).properties(
        width=600,
        height=250
    ).configure_title(
        fontSize=18
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    # Display the chart
    st.header('Tweets per day')
    st.altair_chart(chart, use_container_width=True)

with col3:
    st.header('Pembagian Analisis Sentimen')

    # Process the data
    sentiment_count = df['sentimen'].value_counts().reset_index()
    sentiment_count.columns = ['sentimen', 'count']
    sentiment_count['percentage'] = (sentiment_count['count'] / sentiment_count['count'].sum()) * 100

    # Create the Altair pie chart
    chart = alt.Chart(sentiment_count).mark_arc().encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="sentimen", type="nominal", scale=alt.Scale(scheme='viridis')),
        tooltip=['sentimen', 'count', alt.Tooltip('percentage:Q', format='.2f')]
    ).properties(
        width=250,
        height=250
    )

    # Add percentage labels
    text = chart.mark_text(radius=120, size=14).encode(
        text=alt.Text('percentage:Q', format='.2f%')
    )

    # Combine the pie chart and text
    final_chart = chart + text

    # Display the chart
    st.altair_chart(final_chart, use_container_width=True)
