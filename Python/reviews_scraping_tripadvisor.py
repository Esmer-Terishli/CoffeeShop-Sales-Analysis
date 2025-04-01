import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import csv

BASE_URL = "https://www.tripadvisor.com/FindRestaurants?geo=293934&establishmentTypes=9900&broadened=false"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
OUTPUT_FILENAME = "reviews_scraping_tripadvisor.csv"

def get_next_page_url(soup, base_url, is_reviews_page=False):
    """
    Finds next page URL for either coffeeshop listings or reviews
    """
    next_btn = soup.find("a", {"data-smoke-attr": "pagination-next-arrow"})
    return urljoin(base_url, next_btn.get("href")) if next_btn else None

def extract_coffeeshop_id(url):
    """
    Extracts unique ID from coffee coffeeshop URL
    """
    parts = url.split('-')
    return parts[2][1:] if len(parts) >= 3 and parts[2].startswith('d') else None

def scrape_reviews(coffeeshop_url):
    """
    Scrapes all reviews for a single coffeeshop
    """
    reviews = []
    reviews_url = coffeeshop_url.replace("Restaurant_Review", "Restaurant_Review-all").split("Reviews-")[0] + "Reviews-or1"
    
    while reviews_url:
        try:
            page = requests.get(reviews_url, headers=HEADERS)
            soup = BeautifulSoup(page.content, "html.parser")
            
            if not reviews:
                coffeeshop_name = soup.find("h1", class_="biGQs").text.strip() if soup.find("h1", class_="biGQs") else "N/A"
            
            for review in soup.find_all("div", {"data-automation": "reviewCard"}):
                try:
                    content_div = review.find("div", {"data-test-target": "review-body"})
                    content = ""
                    if content_div:
                        content_span = content_div.find("span", class_="JguWG")
                        if content_span:
                            content = content_span.get_text(separator=" ", strip=True)
                        else:
                            content = content_div.get_text(separator=" ", strip=True)
                    
                    rating_svg = review.find("svg", class_="evwcZ")
                    rating = "N/A"
                    if rating_svg:
                        title_tag = rating_svg.find("title")
                        if title_tag:
                            try:
                                rating = int(title_tag.get_text().split()[0])
                            except (ValueError, IndexError):
                                rating = "N/A"
                    
                    reviews.append({
                        "coffeeshop_name": coffeeshop_name,
                        "coffeeshop_url": coffeeshop_url,
                        "rating": rating,
                        "title": review.find("div", {"data-test-target": "review-title"}).text.strip() if review.find("div", {"data-test-target": "review-title"}) else "N/A",
                        "content": content
                    })
                except Exception as e:
                    print(f"Skipping review - Error: {e}")
                    continue
            
            reviews_url = get_next_page_url(soup, reviews_url, is_reviews_page=True)
            time.sleep(2)
            
        except Exception as e:
            print(f"Failed to process reviews page: {e}")
            break
            
    return reviews

def main():
    """
    Main scraping function
    """
    all_reviews = []
    current_page = BASE_URL
    processed_coffeeshops = set()
    
    print("Starting scrape for all coffeeshops...")
    
    while current_page:
        try:
            response = requests.get(current_page, headers=HEADERS)
            soup = BeautifulSoup(response.content, "html.parser")
            
            for link in soup.select("a[href^='/Restaurant_Review-']"):
                coffeeshop_url = urljoin("https://www.tripadvisor.com", link.get("href").split("#")[0])
                coffeeshop_id = extract_coffeeshop_id(coffeeshop_url)
                
                if coffeeshop_id and coffeeshop_id not in processed_coffeeshops:
                    processed_coffeeshops.add(coffeeshop_id)
                    print(f"\nScraping coffee shop #{len(processed_coffeeshops)}: {coffeeshop_url}")
                    
                    try:
                        coffeeshop_reviews = scrape_reviews(coffeeshop_url)
                        all_reviews.extend(coffeeshop_reviews)
                        print(f"Found {len(coffeeshop_reviews)} reviews (Total: {len(all_reviews)})")
                        time.sleep(3)
                    except Exception as e:
                        print(f"Failed to scrape coffeeshop: {e}")
                        continue
            
            current_page = get_next_page_url(soup, current_page)
            time.sleep(3) 
            
        except Exception as e:
            print(f"Fatal error: {e}")
            break
    
    if all_reviews:
        with open(OUTPUT_FILENAME, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["coffeeshop_name", "coffeeshop_url", "rating", "title", "content"])
            writer.writeheader()
            writer.writerows(all_reviews)
        print(f"\nDone! Saved {len(all_reviews)} reviews from {len(processed_coffeeshops)} coffeeshops to {OUTPUT_FILENAME}")
    else:
        print("No reviews collected.")

if __name__ == "__main__":
    main()