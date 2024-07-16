import requests
from decouple import config
import concurrent.futures

from src.qdrant import upload_website_to_collection, upload_website_to_collection_combined

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


def total_search_news(query, start_date, end_date, source):
    api_key = config("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={query}&from={start_date}&to={end_date}&sources={source}&pageSize=99&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching news from {source}: {response.status_code} - {response.text}")
        return []

    data = response.json()
    if 'articles' not in data:
        print(f"Error: 'articles' key not found in the response from {source}")
        return []

    urls = [article['url'] for article in data['articles']]
    # print(f"URLs from {source} {len(urls)},len{urls}: {urls}")
    print(f"URLs from {source}: {len(urls)}")
    return urls


def upload_news_to_collection_new(query, start_date, end_date):
    sources = ["cnn", "bbc-news", "cbc-news", "al-jazeera-english", "cbs-news", "fox-news","time","usa-today","the-wall-street-journal","reuters"]
    all_urls = []

    for source in sources:
        urls = total_search_news(query, start_date, end_date, source)
        all_urls.extend(urls)

    print(f"Found {len(all_urls)} URLs in total.")

    failed_uploads = []
    successful_uploads = []

    def upload_with_logging(url):
        message, success = upload_website_to_collection_combined(url)
        if success:
            successful_uploads.append(url)
        else:
            print(f"Failed to upload {url}: {message}")
            failed_uploads.append(url)

    # Use ThreadPoolExecutor for parallel uploads
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(upload_with_logging, all_urls)

    if failed_uploads:
        print(f"Failed to upload the following URLs: {failed_uploads}")
    else:
        print("All URLs uploaded successfully.")

    print(f"Successfully uploaded the following URLs: {successful_uploads}")