import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Dashboard Sentiment Analysis GBK",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

col1, col2 = st.columns((6,4), gap='small')
with col2:
    month = st.selectbox("Month:", ('All', 'April', 'Mei', 'Juni'))
    
with col1:
    st.title(f'Sentiment Analysis Dashboard for GBK - {month}' if month != 'All' else 'Sentiment Analysis Dashboard for GBK')

# Load data
if month != 'All':
    file = f"Hasil Sentiment Analysis GBK {month} 2024.xlsx"
    df = pd.read_excel(file)
else:
    df_list = []
    months = ['April', 'Mei', 'Juni']
    for month in months:
        df_awal = pd.read_excel(f"Hasil Sentiment Analysis GBK {month} 2024.xlsx")
        df_list.append(df_awal)
    df = pd.concat(df_list, ignore_index=True)

# Convert 'created_at' to datetime
df['created_at'] = pd.to_datetime(df['created_at'])

# Ensure 'translated_text' is treated as a string and handle NaN values
df['translated_text'] = df['translated_text'].astype(str).fillna('')

# Create bigrams only for non-empty strings
df['bigrams'] = df['translated_text'].apply(lambda x: list(zip(x.split(" ")[:-1], x.split(" ")[1:])) if x.strip() != '' else [])

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["All", "Positive 😊", "Negative ☹️", "Neutral 😐"])

# Layout Columns
col1, col2, col3 = st.columns((2,2,2), gap='large')

with col1:
    st.header('WordCloud')
    all_text = ' '.join(df['full_text'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

with col2:
    st.header('Tweets per Day')
    df['date'] = df['created_at'].dt.date
    tweet_per_day = df.groupby('date').size().reset_index(name='count')

    # Line Chart for Tweets per Day
    chart = alt.Chart(tweet_per_day).mark_line(point=True).encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('count:Q', title='Number of Tweets'),
        tooltip=['date:T', 'count:Q']
    ).properties(
        width=500,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)

with col3:
    st.header('Sentiment Distribution')

    # Pie Chart for Sentiment Distribution
    sentiment_count = df['sentimen'].value_counts().reset_index()
    sentiment_count.columns = ['sentimen', 'count']
    sentiment_count['percentage'] = (sentiment_count['count'] / sentiment_count['count'].sum()) * 100

    chart = alt.Chart(sentiment_count).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="sentimen", type="nominal", scale=alt.Scale(scheme='category20b')),
        tooltip=['sentimen:N', 'count:Q', alt.Tooltip('percentage:Q', format='.2f')]
    ).properties(
        width=300,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)

# Bar Charts for Top Occurring Words and Bigrams
col1, col2 = st.columns((1, 1), gap='large')

with col1:
    st.header('Top 10 Occurring Words')

    top_words = pd.Series(' '.join(df['translated_text'].dropna()).lower().split()).value_counts().reset_index()
    top_words.columns = ['Word', 'Count']
    top_words = top_words.head(10)

    bar_chart_words = alt.Chart(top_words).mark_bar().encode(
        x=alt.X('Count:Q', title='Count'),
        y=alt.Y('Word:N', sort='-x', title='Top 10 Occurring Words')
    ).properties(
        width=400,
        height=300
    )

    st.altair_chart(bar_chart_words, use_container_width=True)

with col2:
    st.header('Top 10 Occurring Bigrams')

    df['bigrams'] = df['translated_text'].apply(lambda x: list(zip(x.split(" ")[:-1], x.split(" ")[1:])))
    bigrams = pd.Series([f"{x[0]} {x[1]}" for sublist in df['bigrams'] for x in sublist]).value_counts().reset_index()
    bigrams.columns = ['Bigram', 'Count']
    top_bigrams = bigrams.head(10)

    bar_chart_bigrams = alt.Chart(top_bigrams).mark_bar().encode(
        x=alt.X('Count:Q', title='Count'),
        y=alt.Y('Bigram:N', sort='-x', title='Top 10 Occurring Bigrams')
    ).properties(
        width=400,
        height=300
    )

    st.altair_chart(bar_chart_bigrams, use_container_width=True)

# Display Tweets Table
st.header('Tweets')
st.write(df[['sentimen', 'translated_text']].head(10))
