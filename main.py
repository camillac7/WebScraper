#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse

def scrape_website(url, selector=None):
    """
    Scrape a website and extract content.
    
    Args:
        url: The URL to scrape
        selector: Optional CSS selector to find specific elements
    """
    try:
        # Send a GET request to the website
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if selector:
            # Find elements using CSS selector
            elements = soup.select(selector)
            results = [elem.get_text(strip=True) for elem in elements]
            return results
        else:
            # Return all text content
            return soup.get_text(separator='\n', strip=True)
            
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    except Exception as e:
        print(f"Error parsing the content: {e}")
        return None

def scrape_links(url):
    """Extract all links from a webpage."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)
            # Convert relative URLs to absolute
            absolute_url = urljoin(url, href)
            links.append({
                'text': text,
                'url': absolute_url
            })
        
        return links
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Main function to run the scraper."""
    print("=== Simple Web Scraper ===\n")
    
    # Example 1: Scrape a simple website
    print("Example 1: Scraping example.com")
    url = "https://example.com"
    content = scrape_website(url)
    if content:
        print(f"First 200 characters:\n{content[:200]}...\n")
    
    # Example 2: Extract specific elements (headings)
    print("\nExample 2: Extracting headings from example.com")
    headings = scrape_website(url, selector="h1, h2, h3")
    if headings:
        for heading in headings:
            print(f"  - {heading}")
    
    # Example 3: Extract links
    print("\nExample 3: Extracting links from example.com")
    links = scrape_links(url)
    if links:
        print(f"Found {len(links)} links:")
        for link in links[:5]:  # Show first 5 links
            print(f"  - {link['text']}: {link['url']}")
    
    print("\n=== Try your own URL ===")
    print("Modify the URL in main() to scrape different websites!")
    print("Example: scrape_website('https://quotes.toscrape.com', 'span.text')")

if __name__ == "__main__":
    main()

