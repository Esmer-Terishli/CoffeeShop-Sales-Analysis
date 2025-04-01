from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import pandas as pd

# Chrome configuration
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-webgl")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--use-gl=disabled")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service(r"C:\Users\ASUS\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Target drinks with all variants (multi-word variants included as single strings)
target_drinks = {
    "americano", "amerikano", "american", "amerikan",
    "latte", "caffelatte", "caffe latte", "espresso",
    "cappuccino", "cappucino", "kapuçino", "kappuçino", "kappuchino",
    "rafcoffee", "raf coffee", "rafkofe", "raf kofe", "rafqəhvəsi", "raf qəhvəsi", "raf",
    "whitemocha", "white mocha", "ağşokoladlımoka", "ağ şokoladlı moka",
    "blackmocha", "black mocha",
    "hotchocolate", "hot chocolate", "ısti şokolad", "i̇sti şokolad", "ıstişokolad", "istişokolad",
    "tea", "blacktea", "black tea", "qaraçay", "qara çay", "çay"
}

def extract_price(price_text):
    """
    Extracts and converts the price from a text string to a float.
    Returns None if no valid price is found.
    """
    match = re.search(r"(\d+[\.,]?\d*)", price_text.replace(" ", ""))
    return float(match.group(1).replace(",", ".")) if match else None

def clean_product_name(name):
    """
    Cleans the product name by removing special characters and converting to lowercase.
    """
    return re.sub(r"[^a-zA-Z0-9ğüşöçıİƏə ]", "", name.lower()).strip()

def get_coffeeshops():
    """
    Retrieves and returns unique coffeeshop links from a webpage by scrolling and collecting URLs.
    """
    print("Accessing the coffeeshop page...")
    driver.get("https://wolt.com/ru/discovery/category/cafe")
    time.sleep(5)

    scroll_attempts = 0
    max_scroll_attempts = 30
    last_height = driver.execute_script("return document.body.scrollHeight")

    print("Scrolling through the page...")
    while scroll_attempts < max_scroll_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        try:
            show_more = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='category-page-show-more-button']"))
            )
            show_more.click()
            print("'Show more' button found and clicked")
            time.sleep(3)
        except:
            pass

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scroll_attempts += 1
            print(f"Same page height ({scroll_attempts}/{max_scroll_attempts})")
        else:
            scroll_attempts = 0
        last_height = new_height

        if scroll_attempts > 5:
            break

    print("Collecting coffeeshop links...")
    coffeeshop_links = set()
    attempts = 0

    while attempts < 3:
        elements = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/restaurant/')]"))
        )

        new_links = {el.get_attribute("href") for el in elements
                     if '/ru/aze/baku/restaurant/' in el.get_attribute("href")}

        if new_links and len(new_links) > len(coffeeshop_links):
            coffeeshop_links.update(new_links)
            attempts = 0
        else:
            attempts += 1

        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)

    print(f"Total unique coffeeshops found: {len(coffeeshop_links)}")
    return list(coffeeshop_links)

def get_menu_items(url):
    print(f"\nRetrieving menu details: {url}")
    driver.get(url)
    try:
        name = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.habto2o span"))
        ).text

        items = []
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-test-id='horizontal-item-card'], div.menu-item"))
        )

        for product in products:
            try:
                product_name = product.find_element(By.CSS_SELECTOR, "h3[data-test-id='horizontal-item-card-header'], h3.item-card-header").text
                cleaned_name = clean_product_name(product_name)

                matched_drink = None
                for target in target_drinks:
                    if target in cleaned_name:
                        matched_drink = target
                        break

                if matched_drink:
                    price_text = product.find_element(
                        By.CSS_SELECTOR,
                        "span[data-test-id='horizontal-item-card-price'], span.item-card-price"
                    ).text
                    price = extract_price(price_text)
                    items.append((product_name, price, matched_drink))
            except Exception as e:
                continue

        return name, items
    except Exception as e:
        print(f"Error retrieving menu: {str(e)}")
        return None, []

print("Program is starting...")
try:
    print("Searching for coffeeshops...")
    all_coffeeshops = get_coffeeshops()
    print(f"Total coffeeshops found: {len(all_coffeeshops)}")


    csv_columns = [
        "CoffeeShop Name", "Americano", "Latte", "Espresso", "Cappuccino",
        "Raf Coffee", "White Mocha", "Black Mocha", "Hot Chocolate", "Tea"
    ]

    drink_mapping = {
        "americano": "Americano",
        "amerikano": "Americano",
        "american": "Americano",
        "amerikan": "Americano",
        "latte": "Latte",
        "caffelatte": "Latte",
        "caffe latte": "Latte",
        "espresso": "Espresso",
        "cappuccino": "Cappuccino",
        "cappucino": "Cappuccino",
        "kapuçino": "Cappuccino",
        "kappuçino": "Cappuccino",
        "kappuchino": "Cappuccino",
        "rafcoffee": "Raf Coffee",
        "raf coffee": "Raf Coffee",
        "rafkofe": "Raf Coffee",
        "raf kofe": "Raf Coffee",
        "rafqəhvəsi": "Raf Coffee",
        "raf qəhvəsi": "Raf Coffee",
        "raf": "Raf Coffee",
        "whitemocha": "White Mocha",
        "white mocha": "White Mocha",
        "ağşokoladlımoka": "White Mocha",
        "ağ şokoladlı moka": "White Mocha",
        "blackmocha": "Black Mocha",
        "black mocha": "Black Mocha",
        "hotchocolate": "Hot Chocolate",
        "hot chocolate": "Hot Chocolate",
        "ısti şokolad": "Hot Chocolate",
        "i̇sti şokolad": "Hot Chocolate",
        "ıstişokolad": "Hot Chocolate",
        "istişokolad": "Hot Chocolate",
        "tea": "Tea",
        "blacktea": "Tea",
        "black tea": "Tea",
        "qaraçay": "Tea",
        "qara çay": "Tea",
        "çay": "Tea"
    }

    data = []
    for i, url in enumerate(all_coffeeshops, 1):
        print(f"\nProcessing {i}/{len(all_coffeeshops)}: {url}")
        name, items = get_menu_items(url)
        if not name:
            print(f"Error: CoffeeShop name not found - {url}")
            continue

        row = {"CoffeeShop Name": name}
        for drink in csv_columns[1:]:
            row[drink] = pd.NA

        for product_name, price, matched_target in items:
            column_name = drink_mapping.get(matched_target)
            if column_name and pd.isna(row[column_name]):
                row[column_name] = price
                print(f"Found: {product_name} → {column_name} ({price} AZN)")
        data.append(row)

    df = pd.DataFrame(data, columns=csv_columns)
    print(df)
    output_file = 'wolt_prices_scraping.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nResults have been written to '{output_file}' file. Total number of coffeeshops processed: {len(data)}")

except Exception as e:
    print(f"Main program error: {str(e)}")

finally:
    driver.quit()
    print("Browser closed. Program finished.")