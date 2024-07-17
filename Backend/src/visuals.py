# import pandas as pd
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
    df['polarity_category'] = df['polarity'].apply(classify_polarity)

    return df

def plot_sentiment_polarity_distribution(df):
    polarity_counts = df['polarity_category'].value_counts().reset_index()
    polarity_counts.columns = ['polarity_category', 'count']
    
    fig = px.pie(
        polarity_counts,
        names='polarity_category',
        values='count',
        title='Sentiment Polarity Distribution'
    )
    buf = BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

# Perform sentiment analysis
detailed_joe_biden_articles_sentiment = perform_sentiment_analysis(detailed_joe_biden_articles)



# import pandas as pd
# from urllib.parse import urlparse
# import plotly.express as px
# import pickle
# from alldocuments import load_cached_data, retrieve_all_documents, combined_collection_name, cache_data
# from textblob import TextBlob

# # Retrieve or load cached data
# detailed_joe_biden_articles = load_cached_data()
# if detailed_joe_biden_articles is None:
#     detailed_joe_biden_articles = retrieve_all_documents(combined_collection_name)
#     cache_data(detailed_joe_biden_articles)

# print(detailed_joe_biden_articles.shape)

# # Function to extract domain from a URL
# def extract_domain(url):
#     try:
#         return urlparse(url).netloc
#     except:
#         return None
    
# def plot_source_urls(data):

#     # Get the source domains from the metadata
#     detailed_joe_biden_articles['domain'] = detailed_joe_biden_articles['metadata'].apply(lambda x: extract_domain(x['source_url']))

#     # Count the occurrences of each domain
#     domain_counts = detailed_joe_biden_articles['domain'].value_counts().head(15)  # Show top 15 domains

#     # Create a bar chart
#     fig = px.bar(x=domain_counts.index, y=domain_counts.values, labels={'x': 'Source', 'y': 'Count'}, title='Top Source Domain Distribution')
#     fig.show()

# # plot_source_urls(detailed_joe_biden_articles)

# def perform_sentiment_analysis(df):
#     def extract_text_content(row):
#         return row['page_content']

#     def classify_polarity(polarity):
#         if polarity > 0:
#             return 'Positive'
#         elif polarity < 0:
#             return 'Negative'
#         else:
#             return 'Neutral'

#     df['text_content'] = df.apply(extract_text_content, axis=1)
#     df['polarity'] = df['text_content'].apply(lambda text: TextBlob(text).sentiment.polarity)
#     df['polarity_category'] = df['polarity'].apply(classify_polarity)

#     return df

# def plot_sentiment_polarity_distribution(df):
#     def extract_text_content(row):
#         return row['page_content']

#     def classify_polarity(polarity):
#         if polarity > 0:
#             return 'Positive'
#         elif polarity < 0:
#             return 'Negative'
#         else:
#             return 'Neutral'
        
#     polarity_counts = df['polarity_category'].value_counts()
#     fig = px.pie(
#         names=polarity_counts.index,
#         values=polarity_counts.values,
#         title='Sentiment Polarity Distribution'
#     )
#     fig.show()

#     df['text_content'] = df.apply(extract_text_content, axis=1)
#     df['polarity'] = df['text_content'].apply(lambda text: TextBlob(text).sentiment.polarity)
#     df['polarity_category'] = df['polarity'].apply(classify_polarity)

#     return df

# # Function to plot sentiment polarity distribution
# def plot_sentiment_polarity_distribution(df):
#     print("Plotting sentiment polarity distribution...")
#     df.to_csv('sentiment.csv', index=False)
#     polarity_counts = df['polarity_category'].value_counts().reset_index()
#     polarity_counts.columns = ['polarity_category', 'count']
#     try:
#         fig = px.pie(
#             polarity_counts,
#             names='polarity_category',
#             values='count',
#             title='Sentiment Polarity Distribution'
#         )
#         fig.show()
#         print("Plot displayed successfully!")
#     except Exception as e:
#         print(f"Error plotting sentiment polarity distribution: {e}")




# # Perform sentiment analysis
# detailed_joe_biden_articles = perform_sentiment_analysis(detailed_joe_biden_articles)

# plot_source_urls(detailed_joe_biden_articles)
# plot_sentiment_polarity_distribution(detailed_joe_biden_articles)