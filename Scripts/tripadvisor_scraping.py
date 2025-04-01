import requests
from bs4 import BeautifulSoup
import time
import csv

BASE_URL = "https://www.tripadvisor.com/FindRestaurants?geo=293934&establishmentTypes=9900&broadened=false"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# List of all possible features
ALL_FEATURES = [
    "Accepts Credit Cards", "Seating", "Free Wifi", "Visa", "Mastercard", 
    "Delivery", "Takeout", "Reservations", "Street Parking", 
    "Non-smoking restaurants", "Parking Available", "Family style", 
    "Digital Payments", "Table Service", "Wine and Beer", "Serves Alcohol", 
    "Outdoor Seating", "American Express", "Dog Friendly", "Full Bar", 
    "Wheelchair Accessible", "Cash Only", "Discover", "Free off-street parking", 
    "Drive Thru", "Television", "Live Music", "Highchairs Available", 
    "Gift Cards Available", "Private Dining", "Playgrounds", "Buffet", 
    "Sports bars", "Jazz Bar", "Validated Parking", "Valet Parking", 
    "Waterfront", "Beach"
]

processed_restaurants = set()

def get_next_page_url(soup):
    next_button = soup.find("a", {"aria-label": "Next page"})
    if next_button:
        return "https://www.tripadvisor.com" + next_button.get("href")
    return None

def create_feature_dict(features_list):
    """
    Create a dictionary with all features set to 0, then update with actual features
    """
    features_dict = {feature: 0 for feature in ALL_FEATURES}
    for feature in features_list:
        if feature in features_dict:
            features_dict[feature] = 1
    return features_dict

def extract_restaurant_id(url):
    """
    Extract unique restaurant ID from URL
    """
    parts = url.split('-')
    if len(parts) >= 3 and parts[2].startswith('d'):
        return parts[2][1:]
    return None

with open('tripadvisor_scraping.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    header = [
        "CoffeeShop Name", "URL", "Address", "Phone", 
        "Rating", "Review count", 
        "Excellent Reviews", "Good Reviews", "Average Reviews", 
        "Poor Reviews", "Terrible Reviews"
    ] + ALL_FEATURES
    writer.writerow(header)

    current_url = BASE_URL
    coffee_shops_scraped = 0

    while current_url:
        try:
            response = requests.get(current_url, headers=HEADERS)
            soup = BeautifulSoup(response.content, "html.parser")

            for link in soup.select("a[href^='/Restaurant_Review-']"):
                href = link.get("href")
                restaurant_url = "https://www.tripadvisor.com" + href
                
                restaurant_id = extract_restaurant_id(restaurant_url)
                
                if not restaurant_id or restaurant_id in processed_restaurants:
                    continue
                
                processed_restaurants.add(restaurant_id)

                try:
                    rest_response = requests.get(restaurant_url, headers=HEADERS)
                    rest_soup = BeautifulSoup(rest_response.content, "html.parser")

                    # CoffeeShop Name
                    try:
                        cshop_name = rest_soup.find("h1", class_="biGQs _P hzzSG rRtyp").text.strip()
                    except AttributeError:
                        cshop_name = "N/A"

                    # Address
                    try:
                        address = rest_soup.find("span", {"data-automation": "restaurantsMapLinkOnName"}).text.strip()
                    except AttributeError:
                        address = "N/A"

                    # Telephone Number
                    try:
                        phone_number = rest_soup.find("a", {"href": lambda x: x and x.startswith("tel:")}).text.strip()
                    except AttributeError:
                        phone_number = "N/A"
                 
                    # Features
                    try:
                        features_section = rest_soup.find_all("div", class_="biGQs _P pZUbB avBIb KxBGd")
                        features_list = [feature.text.strip() for feature in features_section]
                        features = create_feature_dict(features_list)
                    except AttributeError:
                        features = {feature: 0 for feature in ALL_FEATURES}

                    # Rating and Reviews count
                    try:
                        review_data = rest_soup.find_all("div", class_="jxnKb")
                        reviews = {
                            "Excellent": "N/A", 
                            "Good": "N/A", 
                            "Average": "N/A", 
                            "Poor": "N/A", 
                            "Terrible": "N/A"
                        }
                        for data in review_data:
                            rating = data.find("div", class_="Ygqck o W q").text.strip()
                            count = data.find("div", class_="biGQs _P fiohW biKBZ osNWb").text.strip()
                            reviews[rating] = count
                    except AttributeError:
                        reviews = {
                            "Excellent": "N/A", 
                            "Good": "N/A", 
                            "Average": "N/A", 
                            "Poor": "N/A", 
                            "Terrible": "N/A"
                        }

                    # Rating
                    try:
                        ratingg = rest_soup.find("div", class_="biGQs _P fiohW hzzSG uuBRH", attrs={"data-automation": "reviewBubbleScore"}).text.strip()
                    except AttributeError:
                        ratingg = "N/A"

                    # Reviews count
                    try:
                        review_count = rest_soup.find("div", class_="biGQs _P pZUbB KxBGd").find_next("div", class_="biGQs _P pZUbB KxBGd").text.strip()
                        review_count = ''.join(filter(str.isdigit, review_count))
                    except AttributeError:
                        review_count = "N/A"

                    row = [
                        cshop_name, restaurant_url, address, phone_number,
                        ratingg, review_count,
                        reviews.get("Excellent", "N/A"), reviews.get("Good", "N/A"),
                        reviews.get("Average", "N/A"), reviews.get("Poor", "N/A"),
                        reviews.get("Terrible", "N/A")
                    ] + [features[feature] for feature in ALL_FEATURES]

                    writer.writerow(row)
                    coffee_shops_scraped += 1
                    print(f"Scraped {coffee_shops_scraped}: {cshop_name}")
                    
                    time.sleep(2)

                except Exception as e:
                    print(f"Error scraping {restaurant_url}: {str(e)}")
                    continue

            current_url = get_next_page_url(soup)
            if current_url:
                print(f"Moving to next page: {current_url}")
                time.sleep(2)
            else:
                print("No more pages found")

        except Exception as e:
            print(f"Error processing page {current_url}: {str(e)}")
            break

print(f"\nScraping completed! Unique {coffee_shops_scraped} coffee shops saved to tripadvisor_scraping.csv")