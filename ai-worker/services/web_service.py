import requests 
from core.config import settings

def search_tavily(query: str, max_results: int = 3) -> list:
    """Uses Tavily API to search the web and return a list of URLs."""
    if not settings.tavily_api_key:
        print("Warning: TAVILY_API_KEY is not set. Cannot search.")
        return []

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": settings.tavily_api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results
    }

    response = requests.post(url, json=payload, verify=settings.verify_ssl)
    if response.status_code == 200:
        results = response.json().get("results", [])
        return [result["url"] for result in results]
    else:
        print(f"Tavily Search Failed: {response.text}")
        return []

def read_url_with_jina(url: str) -> str:
    """Uses Jina Reader (r.jina.ai) to convert a webpage to Markdown."""
    jina_url = f"https://r.jina.ai/{url}"

    # Using verify=False to bypass firewall as requested
    try:
        response = requests.get(jina_url, verify=settings.verify_ssl, timeout=15)
        if response.status_code == 200:
            return response.text
        return ""
    except Exception as e:
        print(f"Failed to read {url}: {e}")
        return ""
