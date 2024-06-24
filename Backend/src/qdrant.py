from langchain_qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from qdrant_client import QdrantClient, models
from decouple import config
# from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Filter
import string

qdrant_api_key = config("QDRANT_API_KEY")
qdrant_url = config("QDRANT_URL")
collection_name = "Joe Bidens News"

client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)

vector_store = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=OpenAIEmbeddings(
        api_key=config("OPENAI_API_KEY")
    )
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len
)

# def preprocess_text(text):
#     text = text.translate(str.maketrans('', '', string.punctuation)).lower()
#     words = text.split()
#     words = [word for word in words if word not in stop_words]
#     return ' '.join(words)



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


    
# create_collection(collection_name)
# upload_website_to_collection("https://edition.cnn.com/2024/06/21/politics/biden-trump-character-attacks/index.html")
