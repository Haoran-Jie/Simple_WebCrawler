import requests
from bs4 import BeautifulSoup

def crawl(url, max_urls=100):
    # Keep track of how many URLs we've crawled so far
    num_urls_crawled = 0

    # Keep track of the URLs we've already crawled
    # to avoid crawling the same URL more than once
    visited_urls = set()

    # Keep track of the URLs we haven't crawled yet
    # by using a queue data structure
    queue = [url]

    while queue:
        # Pop the first URL from the queue
        current_url = queue.pop(0)

        # Download the current URL's HTML content
        try:
            response = requests.get(current_url)
        except:
            continue

        # Extract the URLs of other pages linked to from the HTML source code
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all()
        for link in links:
            if "href" in link.attrs:
                linked_url = link.attrs["href"]
                if not str(linked_url).startswith("http"):
                    continue
                # Only add the URL to the queue if it hasn't been visited yet
                # and if it's not an empty string
                if linked_url not in visited_urls and linked_url != "":
                    queue.append(linked_url)
                    num_urls_crawled += 1
                    visited_urls.add(linked_url)
                    # Stop crawling and return if we've reached the maximum number of URLs
                    if num_urls_crawled == max_urls:
                        return visited_urls


    return visited_urls

# Crawl the input URL and print the URLs that were discovered
for url in crawl("https://news.ycombinator.com"):
    print(url)
