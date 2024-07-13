import requests
from decouple import config

def get_newsapi_sources():
    api_key = config("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/sources?apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        sources = data.get('sources', [])
        source_names = [source['id'] for source in sources]
        return source_names
    else:
        print(f"Failed to fetch sources: {response.status_code} - {response.text}")
        return []

# Example usage
# sources = get_newsapi_sources()
# print("Available NewsAPI sources:", sources)
