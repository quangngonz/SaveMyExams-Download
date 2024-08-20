import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time, pickle

# To store visited URLs and URLs to visit
visited_urls = set()
urls_to_visit = ["https://www.savemyexams.com"]

# Define a function to crawl a webpage
def crawl(url):
    # Check if the URL has been visited
    if url in visited_urls:
        return

    # Add the URL to the list of visited URLs
    visited_urls.add(url)

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to access {url}: {e}")
        return

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all links from the page
    for link in soup.find_all("a", href=True):
        # Join the URL to handle relative links
        full_url = urljoin(url, link["href"])

        # Filter out external links
        if urlparse(full_url).netloc == urlparse(url).netloc:
            if full_url not in visited_urls:
                urls_to_visit.append(full_url)

    print(f"Visited: {url}")

# Crawl all URLs starting from the initial URL
while urls_to_visit:
    current_url = urls_to_visit.pop(0)
    crawl(current_url)
    time.sleep(1)  # Pause between requests to avoid overloading the server

# Print all accessible URLs
print("\nAccessible URLs:")
for url in visited_urls:
    print(url)

with open("visited_urls.pkl", "wb") as f:
    pickle.dump(visited_urls, f)
