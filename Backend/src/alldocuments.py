from qdrant_client import QdrantClient
from decouple import config
import pandas as pd
import pickle

qdrant_url = config("QDRANT_URL")
qdrant_api_key = config("QDRANT_API_KEY")

combined_collection_name = 'Detailed Joe Bidens News'

client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)

# Function to retrieve all data from a collection
def retrieve_all_documents(collection_name, client=client):
    all_articles = []
    offset = None
    while True:
        response, offset = client.scroll(
            collection_name=collection_name,
            offset=offset,
            with_payload=True,
            limit=1000  # Adjust if needed
        )
        articles = [hit.payload for hit in response]
        all_articles.extend(articles)
        if not offset:
            break
    return pd.DataFrame(all_articles)

# Cache the data
def cache_data(data, filename='cached_data.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

# Load the cached data
def load_cached_data(filename='cached_data.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None







