import pandas as pd
from urllib.parse import urlparse
import plotly.express as px
import pickle
from src.alldocuments import load_cached_data, retrieve_all_documents, combined_collection_name, cache_data
from textblob import TextBlob
import base64
from io import BytesIO

# Retrieve or load cached data
detailed_joe_biden_articles = load_cached_data()
if detailed_joe_biden_articles is None:
    detailed_joe_biden_articles = retrieve_all_documents(combined_collection_name)
    cache_data(detailed_joe_biden_articles)

print(detailed_joe_biden_articles.shape)

# Function to extract domain from a URL
def extract_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return None

def plot_source_urls(data):
    detailed_joe_biden_articles['domain'] = detailed_joe_biden_articles['metadata'].apply(lambda x: extract_domain(x['source_url']))
    # detailed_joe_biden_articles.to_csv('third_sentiment.csv', index=False)
    domain_counts = detailed_joe_biden_articles['domain'].value_counts().head(15)

    fig = px.bar(x=domain_counts.index, y=domain_counts.values, labels={'x': 'Source', 'y': 'Count'}, title='Top Source Domain Distribution')
    buf = BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def perform_sentiment_analysis(df):
    def extract_text_content(row):
        return row['page_content']

    def classify_polarity(polarity):
        if polarity > 0:
            return 'Positive'
        elif polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'

    df['text_content'] = df.apply(extract_text_content, axis=1)
    df['polarity'] = df['text_content'].apply(lambda text: TextBlob(text).sentiment.polarity)
    # df.to_csv('second_sentiment.csv', index=False)
    df['polarity_category'] = df['polarity'].apply(classify_polarity)

    return df

def plot_sentiment_polarity_distribution(df):
    polarity_counts = df['polarity_category'].value_counts().reset_index()
    polarity_counts.columns = ['polarity_category', 'count']
    
    fig = px.pie(
        polarity_counts,
        names='polarity_category',
        values='count',
        title='Overal Sentiment Polarity Distribution'
    )
    buf = BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

# Generate pie charts for sentiment polarity distribution per domain
def plot_sentiment_polarity_per_domain(data):
    data['domain'] = data['metadata'].apply(lambda x: extract_domain(x['source_url']))
    
    # Perform sentiment analysis
    data = perform_sentiment_analysis(data)
    
    # Get top 15 domains
    top_domains = data['domain'].value_counts().head(15).index
    
    pie_charts = {}
    
    for domain in top_domains:
        domain_data = data[data['domain'] == domain]
        polarity_counts = domain_data['polarity_category'].value_counts().reset_index()
        polarity_counts.columns = ['polarity_category', 'count']
        
        fig = px.pie(
            polarity_counts,
            names='polarity_category',
            values='count',
            title=f'Sentiment Polarity Distribution for {domain}'
        )
        buf = BytesIO()
        fig.write_image(buf, format="png")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        pie_charts[domain] = img_base64

    return pie_charts

# Perform sentiment analysis
detailed_joe_biden_articles_sentiment = perform_sentiment_analysis(detailed_joe_biden_articles)


def plot_topic_frequencies():
    topics = [
        "Biden's Press Conferences and Public Appearances",
        "Election and Political Campaigns",
        "Health and Fitness Concerns",
        "Media and Public Opinion",
        "NATO and Foreign Policy",
        "Support and Endorsements",
        "Fundraising and Campaign Finance",
        "Debate Performances",
        "Legislation and Policy Initiatives",
        "Public Appearances and Statements"
    ]

    frequencies = [12, 10, 8, 7, 5, 4, 3, 3, 2, 2]

    df = pd.DataFrame({'Topic': topics, 'Frequency': frequencies})
    # df.to_csv('second_sentiment.csv', index=False)

    fig = px.bar(df, x='Topic', y='Frequency', title='Topic  10 Topics and Frequencies')
    buf = BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64


def stacked_bar():
        # Data for plotting
    data = {
        'Source': ['Al Jazeera', 'Al Jazeera', 'Al Jazeera', 'Al Jazeera', 'CNN', 'CNN', 'CNN', 'CBS News', 'CBS News', 'Time', 'Time', 'Time', 'USA Today', 'Fox News', 'Fox News', 'Fox News'],
        'Topic': ['Economy', 'US Election 2024', 'Presidential Debate', 'International Media Coverage', 'Presidential Debate', "Biden's Health and Performance", 'Election Strategy', 'Presidential Debate Ratings', 'Voter Expectations', "Biden's Debate History", 'Economic Records', 'Political Strategy', 'Presidential Debate Reaction', "Biden's Fitness for Presidency", 'Campaign Strategy', 'Media Coverage'],
        'Count': [4, 6, 5, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }

    df = pd.DataFrame(data)

    # Plotting
    fig = px.bar(df, x='Topic', y='Count', color='Source', title='Coverage of Topics by News Sources', barmode='stack')


    buf = BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return img_base64