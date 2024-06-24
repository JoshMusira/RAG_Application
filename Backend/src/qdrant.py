from langchain_qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from qdrant_client import QdrantClient, models
from decouple import config
# from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Filter
import newsapi
import requests
import openai

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


def upload_website_to_collection(url: str):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load_and_split(text_splitter)
        if not docs:
            return "No documents loaded."

        # Log the number of documents loaded
        print(f"Loaded {len(docs)} documents from {url}.")
        

        for doc in docs:
            doc.metadata = {"source_url": url}
            # Log the content and metadata of each document
            # print(f"Document content: {doc.page_content[:100]}...")  # Log first 100 characters
            # print(f"Document metadata: {doc.metadata}")

        # Assuming the vector_store handles adding documents, otherwise, manually add points
        vector_store.add_documents(docs)

        return f"Successfully uploaded {len(docs)} documents to collection {collection_name}."
    except Exception as e:
        print(f"Error uploading website to collection: {e}")
        raise e


# def upload_website_to_collection(url: str):
#     loader = WebBaseLoader(url)
#     docs = loader.load_and_split(text_splitter)
#     for doc in docs:
#         doc.metadata = {"source_url": url}
    
    
#     return f"Successfully uploaded {len(docs)} documents to collection {collection_name}."

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


def search_news(query, start_date, end_date):
    api_key = config("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={query}&from={start_date}&to={end_date}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    print(data)

    try:
        urls = [article['url'] for article in data['articles']]
        return urls
    except KeyError as e:
        print(f"Error: {e}")
        return []

start_date = "2024-01-01"
end_date = "2024-06-30"

def upload_news_to_collection(url, start_date, end_date):
    print(url)
    # Search for news articles using OpenAI's API
    urls = search_news(url, start_date, end_date)
    print(len(urls))

    # Upload each news article to the collection
    for url in urls:
        upload_website_to_collection(url)


# Example usage:
# query = "Joe Biden OR Donald Trump"


# create_collection(collection_name)
# upload_news_to_collection(query, start_date, end_date)
# create_collection(collection_name)
# upload_website_to_collection("https://edition.cnn.com/2024/06/21/politics/biden-trump-character-attacks/index.html")
