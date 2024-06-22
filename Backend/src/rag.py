import openai
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI
from operator import itemgetter
from decouple import config
from src.qdrant import vector_store
import nltk
from nltk.corpus import stopwords
import string
import base64
from io import BytesIO
from wordcloud import WordCloud, STOPWORDS

# Load stop words
nltk.download('stopwords')
stop_words = set(stopwords.words('english')).union(set(STOPWORDS))

model = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key=config("OPENAI_API_KEY"),
    temperature=0,
    streaming=True
)

prompt_template = """
Answer the question based on the context, in a detailed manner, in markdown and using bullet points where applicable.

Context: {context}
Question: {question}
Answer:
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

retriever = vector_store.as_retriever()

def create_chain():
    chain = (
        {
            "context": retriever.with_config(top_k=4),
            "question": RunnablePassthrough(),
        }
        | RunnableParallel({
            "response": prompt | model,
            "context": itemgetter("context"),
            })
    )
    return chain

def extract_keywords(text):
    openai.api_key = config("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Extract the top 5 themes from the following text:\n\n{text}"}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extracting themes from the response
    themes_content = response.choices[0].message['content']
    themes = themes_content.strip().split('\n')
    
    return themes

def get_answer_and_docs(question: str):
    chain = create_chain()
    response = chain.invoke(question)
    answer = response["response"].content

    # Tokenize the answer text using nltk
    tokens = nltk.word_tokenize(answer)

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
        "word_cloud_image": word_cloud_image
    }
