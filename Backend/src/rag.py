import openai
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI
from operator import itemgetter
from decouple import config
from src.qdrant import vector_store, combined_vector_store
import nltk
from nltk.corpus import stopwords
import string
import base64
from io import BytesIO
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
# Load stop words
nltk.download('stopwords')
stop_words = set(stopwords.words('english')).union(set(STOPWORDS))

model = ChatOpenAI(
    model_name="gpt-4-turbo-preview",
    openai_api_key=config("OPENAI_API_KEY"),
    temperature=0,
    streaming=True
)

prompt_template = """
Answer the question based on the context and timestamps (day, week, month, quarter, year, etc.) provided by the user. Keep in mind the year or entire date provided in the user's documents. Only answer the question as asked, without giving wrong answers or incorrect timestamp references. If only a year is provided, interpret it accordingly. Summarize the information in a detailed manner, in markdown format and give good formats depending on the question asked, and use bullet points where applicable.

Context: {context}
Question: {question}
Answer:
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

retriever = vector_store.as_retriever( search_kwargs={'k': 30})
retrieverCombined = combined_vector_store.as_retriever( search_kwargs={'k': 80})

def create_chain():
    chain = (
        {
            "context": retriever.with_config(),
            "question": RunnablePassthrough(),
        }
        | RunnableParallel({
            "response": prompt | model,
            "context": itemgetter("context"),
            })
    )
    return chain

def create_chain2():
    chain = (
        {
            "context": retrieverCombined.with_config(),
            "question": RunnablePassthrough(),
        }
        | RunnableParallel({
            "response": prompt | model,
            "context": itemgetter("context"),
            })
    )
    return chain

def extract_keywords(text, n_keywords=5):
    vectorizer = TfidfVectorizer(stop_words=list(stop_words))
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray().flatten()
    keyword_indices = scores.argsort()[-n_keywords:][::-1]
    keywords = [feature_names[i] for i in keyword_indices]
    return keywords


def get_answer_and_docs(question: str):
    chain = create_chain()
    response = chain.invoke(question)
    answer = response["response"].content
    context = response["context"]

    # Tokenize the answer text using nltk
    tokens = nltk.word_tokenize(answer)
    # Extract keywords
    keywords = extract_keywords(answer)

    # Remove stop words manually
    tokens = [word for word in tokens if word.lower() not in stop_words and word.isalnum()]

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, max_words=200, font_step=1, min_font_size=20, max_font_size=100, random_state=42).generate(' '.join(tokens))

    # Convert the word cloud to a base64-encoded string
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format="PNG")
    word_cloud_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "answer": answer,
        "context": response["context"],
        "word_cloud_image": word_cloud_image,
        "keywords": keywords
    }


def get_answer_and_docs_combined(question: str):
    chain = create_chain2()
    response = chain.invoke(question)
    answer = response["response"].content
    context = response["context"]

    # Tokenize the answer text using nltk
    tokens = nltk.word_tokenize(answer)
    # Extract keywords
    keywords = extract_keywords(answer)

    # Remove stop words manually
    tokens = [word for word in tokens if word.lower() not in stop_words and word.isalnum()]

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, max_words=200, font_step=1, min_font_size=20, max_font_size=100, random_state=42).generate(' '.join(tokens))

    # Convert the word cloud to a base64-encoded string
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format="PNG")
    word_cloud_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "answer": answer,
        "context": response["context"],
        "word_cloud_image": word_cloud_image,
        "keywords": keywords
    }


