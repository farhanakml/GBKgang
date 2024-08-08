import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Membaca data dari file CSV
# Ubah 'data.csv' menjadi path file Anda
df = pd.read_excel('Hasil Sentiment Analysis GBK Juni 2024.xlsx')

# Convert 'created_at' ke datetime
df['created_at'] = pd.to_datetime(df['created_at'])

# Menampilkan WordCloud
st.title('Sentiment Analysis Dashboard for GBK')

st.header('WordCloud')
all_text = ' '.join(df['full_text'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(all_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)

# Grafik jumlah tweet per hari
st.header('Jumlah Tweet per Hari')
df['date'] = df['created_at'].dt.date
tweet_per_day = df.groupby('date').size().reset_index(name='count')

plt.figure(figsize=(10, 5))
sns.lineplot(data=tweet_per_day, x='date', y='count', marker='o')
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.title('Number of Tweets per Day')
st.pyplot(plt)

# Pembagian sentimen
st.header('Pembagian Analisis Sentimen')
sentiment_count = df['sentimen'].value_counts()

plt.figure(figsize=(10, 5))
sns.barplot(x=sentiment_count.index, y=sentiment_count.values, palette='viridis')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.title('Sentiment Distribution')
st.pyplot(plt)
