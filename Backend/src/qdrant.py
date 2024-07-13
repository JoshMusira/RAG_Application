from langchain_qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from qdrant_client import QdrantClient, models
from decouple import config
from requests.exceptions import RequestException
import time
from qdrant_client.http.models import Filter
import random

combined_collection_name = 'Detailed Joe Bidens News'
qdrant_api_key = config("QDRANT_API_KEY")
qdrant_url = config("QDRANT_URL")
collection_name = "Joe Bidens News"
openai_api_key = config("OPENAI_API_KEY")

client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)

vector_store = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=OpenAIEmbeddings(
        api_key=openai_api_key
    )
)

combined_vector_store = Qdrant(
    client=client,
    collection_name=combined_collection_name,
    embeddings=OpenAIEmbeddings(
        api_key=openai_api_key
    )
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len
)


def create_collection(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=1536,
            distance=models.Distance.COSINE
        )
    )
    return f"Collection {collection_name} created successfully."

def upload_website_to_collection(url: str, batch_size=5, max_retries=5):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load_and_split(text_splitter)
        if not docs:
            return "No documents loaded.", False
        
        # Add metadata to each document
        for doc in docs:
            doc.metadata = {"source_url": url}

        # Log the number of documents loaded
        print(f"Loaded {len(docs)} documents from {url}.")

        for i in range(0, len(docs), batch_size):
            batch = docs[i:i + batch_size]
            for attempt in range(max_retries):
                try:
                    vector_store.add_documents(batch)
                    print(f"Successfully uploaded batch {i // batch_size + 1} of {len(docs) // batch_size + 1}")
                    break
                except RequestException as e:
                    print(f"Error uploading batch {i // batch_size + 1} (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        sleep_time = (2 ** attempt) + random.uniform(0, 1)
                        print(f"Retrying in {sleep_time:.2f} seconds...")
                        time.sleep(sleep_time)  # Exponential backoff with jitter
                    else:
                        raise e
        return f"Successfully uploaded {len(docs)} documents to collection {collection_name}.", True
    except Exception as e:
        print(f"Error uploading website to collection: {e}")
        return str(e), False
    

def upload_website_to_collection_combined(url: str, batch_size=5, max_retries=5):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load_and_split(text_splitter)
        if not docs:
            return "No documents loaded.", False
        
        # Add metadata to each document
        for doc in docs:
            doc.metadata = {"source_url": url}

        # Log the number of documents loaded
        print(f"Loaded {len(docs)} documents from {url}.")

        for i in range(0, len(docs), batch_size):
            batch = docs[i:i + batch_size]
            for attempt in range(max_retries):
                try:
                    combined_vector_store.add_documents(batch)
                    print(f"Successfully uploaded batch {i // batch_size + 1} of {len(docs) // batch_size + 1}")
                    break
                except RequestException as e:
                    print(f"Error uploading batch {i // batch_size + 1} (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        sleep_time = (2 ** attempt) + random.uniform(0, 1)
                        print(f"Retrying in {sleep_time:.2f} seconds...")
                        time.sleep(sleep_time)  # Exponential backoff with jitter
                    else:
                        raise e
        return f"Successfully uploaded {len(docs)} documents to collection {collection_name}.", True
    except Exception as e:
        print(f"Error uploading website to collection: {e}")
        return str(e), False

def delete_collection_content(collection_name):
    try:
        # Check if the collection exists
        collections = client.get_collections()
        if collection_name not in [collection.name for collection in collections.collections]:
            return f"Collection {collection_name} does not exist."

        # Delete the content of the collection
        client.delete(
            collection_name=collection_name,
            points_selector=Filter()  # This will delete all points in the collection
        )
        return f"Content of collection {collection_name} deleted successfully."
    except Exception as e:
        # Log the exception and re-raise it
        print(f"Error deleting collection content: {e}")
        raise e


def count_unique_urls():
    try:
        # Initialize variables for pagination
        unique_urls = set()
        next_page_token = None

        while True:
            # Retrieve a batch of documents from the collection
            response = client.scroll(
                collection_name=collection_name,
                limit=100,  # Adjust limit as needed
                offset=next_page_token,
                with_payload=True,
                with_vectors=False
            )
            documents, next_page_token = response

            # Extract URLs from metadata and add to the set of unique URLs
            for doc in documents:
                if 'metadata' in doc.payload and 'source_url' in doc.payload['metadata']:
                    unique_urls.add(doc.payload['metadata']['source_url'])

            # If next_page_token is None, we have reached the end of the collection
            if next_page_token is None:
                break

        return f" {len(unique_urls)}"
    except Exception as e:
        print(f"Error counting unique URLs: {e}")
        return str(e)


def count_unique_urls_combined():
    try:
        # Initialize variables for pagination
        unique_urls = set()
        next_page_token = None

        while True:
            # Retrieve a batch of documents from the collection
            response = client.scroll(
                collection_name=combined_collection_name,
                limit=100,  # Adjust limit as needed
                offset=next_page_token,
                with_payload=True,
                with_vectors=False
            )
            documents, next_page_token = response

            # Extract URLs from metadata and add to the set of unique URLs
            for doc in documents:
                if 'metadata' in doc.payload and 'source_url' in doc.payload['metadata']:
                    unique_urls.add(doc.payload['metadata']['source_url'])

            # If next_page_token is None, we have reached the end of the collection
            if next_page_token is None:
                break

        return f" {len(unique_urls)}"
    except Exception as e:
        print(f"Error counting unique URLs: {e}")
        return str(e)



    

# Example usage:
# query = "Joe Biden OR Donald Trump"
# start_date = "2024-06-01"
# end_date = "2024-06-22"
# combined_collection_name = 'Detailed Joe Bidens News'
# create_collection(combined_collection_name)
# upload_news_to_collection(query, start_date, end_date)
# create_collection(collection_name)
# upload_website_to_collection("https://edition.cnn.com/2024/06/21/politics/biden-trump-character-attacks/index.html")
