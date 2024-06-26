import requests
from decouple import config
import concurrent.futures

from src.qdrant import upload_website_to_collection

def search_news(query, start_date, end_date):
    api_key = config("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={query}&from={start_date}&to={end_date}&sources=cnn&pageSize=90&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    try:
        urls = [article['url'] for article in data['articles']]
        print(urls)
        return urls
    except KeyError as e:
        print(f"Error: {e}")
        return []

def upload_news_to_collection(query, start_date, end_date):
    urls = search_news(query, start_date, end_date)
    print(f"Found {len(urls)} URLs.")

    failed_uploads = []
    successful_uploads = []

    def upload_with_logging(url):
        message, success = upload_website_to_collection(url)
        if success:
            successful_uploads.append(url)
        else:
            print(f"Failed to upload {url}: {message}")
            failed_uploads.append(url)

    # Use ThreadPoolExecutor for parallel uploads
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(upload_with_logging, urls)

    if failed_uploads:
        print(f"Failed to upload the following URLs: {failed_uploads}")
    else:
        print("All URLs uploaded successfully.")

    print(f"Successfully uploaded the following URLs: {successful_uploads}")
