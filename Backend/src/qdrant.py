from langchain_qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from qdrant_client import QdrantClient, models
from decouple import config


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

def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)



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
    loader = WebBaseLoader(url)
    docs = loader.load_and_split(text_splitter)
    for doc in docs:
        doc.metadata = {"source_url": url}
    
    
    return f"Successfully uploaded {len(docs)} documents to collection {collection_name}."

# create_collection(collection_name)
# upload_website_to_collection("https://edition.cnn.com/2024/06/21/politics/biden-trump-character-attacks/index.html")
