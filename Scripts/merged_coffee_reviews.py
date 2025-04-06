import pandas as pd
import random
import numpy as np

REVIEWS_FILE = 'C:/Users/ASUS/Desktop/CoffeeShop Sales Analysis/Data/processed/reviews_scraping_tripadvisor.csv'
SALES_FILE = 'C:/Users/ASUS/Desktop/CoffeeShop Sales Analysis/Data/raw/coffeeshop_sales.csv'
OUTPUT_FILE = 'C:/Users/ASUS/Desktop/CoffeeShop Sales Analysis/Data/processed/merged_coffeeshop_reviews.csv'

REVIEW_TYPE_DIST = ['positive']*60 + ['neutral']*25 + ['negative']*15

POSITIVE_TITLES = [
    "Exceptional coffee experience", "Perfect morning ritual", "Absolute must-visit",
    "Coffee perfection achieved", "Barista mastery on display", "Worth waking up early for",
    "Flavor explosion in every cup", "My happy place", "Consistent excellence",
    "Attention to detail shines", "Worth every penny", "Top-tier coffee craftsmanship",
    "A cut above the rest", "Daily dose of happiness", "Coffee nirvana",
    "Elevated coffee experience", "Pure brewing artistry", "Unmatched quality",
    "Coffee lover's paradise", "The gold standard", "Warm atmosphere, cooler drinks",
    "Precision in every pour", "My office away from home", "Specialty coffee done right",
    "Aroma that stops you in your tracks", "Worth the detour", "Perfectly balanced flavors",
    "Staff that remembers your name", "Coffee that makes you smile", "The complete package"
]

NEUTRAL_TITLES = [
    "Standard coffee experience", "Met basic expectations", "Adequate for caffeine needs",
    "Nothing extraordinary", "Middle-of-the-road", "Serviceable coffee stop",
    "Exactly what you'd expect", "No surprises here", "Gets the job done",
    "Average across the board", "Basic but functional", "Unremarkable but fine",
    "Consistently average", "Does what it says", "Coffee without frills",
    "Predictable quality", "Neither impressed nor disappointed", "Standard chain quality",
    "Forgettable but acceptable", "Not bad, not great", "Basic caffeine delivery",
    "Typical coffee shop", "What you see is what you get", "Meets minimum requirements",
    "Passable experience", "Won't wow you", "Doesn't stand out",
    "Average price, average quality", "Satisfactory but not special", "Just okay"
]

NEGATIVE_TITLES = [
    "Disappointing experience", "Wouldn't recommend", "Failed to impress",
    "Overpromised and underdelivered", "Not worth the price", "Mediocre at best",
    "Service needs work", "Quality control issues", "Inconsistent results",
    "Lacking attention to detail", "Poor value proposition", "Unpleasant atmosphere",
    "Rushed and careless", "My last visit here", "Better options available",
    "Missed the mark", "Subpar experience", "Frustrating visit",
    "Won't be returning", "Let down by quality", "Not up to standards",
    "Overcrowded and understaffed", "Dirty equipment", "Inattentive service",
    "Burnt and bitter", "Cold and stale", "Wrong order twice",
    "Uncomfortable seating", "Long wait times", "Save your money"
]

POSITIVE_CONTENT = [
    "Every visit exceeds my already high expectations - the coffee here is truly exceptional.",
    "The baristas demonstrate genuine passion for their craft, resulting in perfect drinks every time.",
    "From the welcoming atmosphere to the carefully sourced beans, this place gets everything right.",
    "I've traveled the world tasting coffee, and this shop ranks among the very best I've experienced.",
    "Attention to detail is remarkable - from precise brewing temps to beautiful latte art.",
    "The owner clearly cares about quality, and it shows in every aspect of the experience.",
    "My daily latte is consistently creamy, well-balanced, and served at the perfect temperature.",
    "They've mastered the difficult balance between professional expertise and warm hospitality.",
    "The seasonal specials always surprise and delight with creative flavor combinations.",
    "As a coffee professional myself, I can attest to their technical excellence and consistency."
]

NEUTRAL_CONTENT = [
    "This coffee shop meets basic expectations without particularly standing out in any way.",
    "The drinks are acceptable though not memorable - exactly what you'd expect from a chain.",
    "I come here because it's convenient, not because the coffee is anything special.",
    "Service is efficient if not particularly warm or engaging - they get the job done.",
    "The space is clean and functional though not especially inviting or comfortable.",
    "Coffee quality varies slightly by barista but generally stays within acceptable parameters.",
    "Prices align with the quality received - neither a bargain nor a rip-off.",
    "It serves its purpose as a place to grab a decent cup and get some work done.",
    "The menu offers standard options without any particularly interesting innovations.",
    "My experiences here have been perfectly adequate though never noteworthy."
]

NEGATIVE_CONTENT = [
    "The espresso tasted burnt and bitter, suggesting the machine needs maintenance.",
    "Staff seemed more interested in their phones than in providing decent service.",
    "At these prices, I expected significantly better quality and attention to detail.",
    "My cappuccino arrived with poorly textured milk and a weak, under-extracted shot.",
    "The shop was uncomfortably crowded with nowhere to sit despite the high prices.",
    "Dirty tables and sticky floors created an unpleasant dining environment.",
    "After waiting 20 minutes for a simple order, the drink was made incorrectly.",
    "The pastries appeared stale and were served without being properly warmed.",
    "Loud music and uncomfortable seating made it impossible to relax or concentrate.",
    "Multiple basic errors in drink preparation suggest inadequate staff training."
]

def generate_url(shop_name):
    """Generate Tripadvisor URL keeping same structure but changing shop name"""
    base = "https://www.tripadvisor.com/Restaurant_Review-g293934-d6522592-Reviews-"
    formatted = shop_name.replace(" ", "_").replace("&", "and").replace("'", "")
    return f"{base}{formatted}-Baku_Absheron_Region.html"

def generate_review(review_type=None):
    """Generate a complete review with consistent sentiment"""
    if not review_type:
        review_type = random.choice(REVIEW_TYPE_DIST)
    
    if review_type == 'positive':
        return {
            'rating': random.randint(4, 5),
            'title': random.choice(POSITIVE_TITLES),
            'content': random.choice(POSITIVE_CONTENT),
            'ReviewType': 'positive'
        }
    elif review_type == 'neutral':
        return {
            'rating': random.randint(2, 4),
            'title': random.choice(NEUTRAL_TITLES),
            'content': random.choice(NEUTRAL_CONTENT),
            'ReviewType': 'neutral'
        }
    else:  # negative
        return {
            'rating': random.randint(1, 2),
            'title': random.choice(NEGATIVE_TITLES),
            'content': random.choice(NEGATIVE_CONTENT),
            'ReviewType': 'negative'
        }

def fill_missing_values(row):
    """Fill missing values in a row while preserving existing values"""
    if pd.isnull(row['coffeeshop_url']):
        row['coffeeshop_url'] = generate_url(row['coffeeshop_name'])
    
    review_type = row['ReviewType'] if pd.notnull(row['ReviewType']) else random.choice(REVIEW_TYPE_DIST)
    row['ReviewType'] = review_type
    
    review_data = generate_review(review_type)
    if pd.isnull(row['rating']):
        row['rating'] = review_data['rating']
    if pd.isnull(row['title']):
        row['title'] = review_data['title']
    if pd.isnull(row['content']):
        row['content'] = review_data['content']
    
    return row

reviews_df = pd.read_csv(REVIEWS_FILE) if REVIEWS_FILE else None
sales_df = pd.read_csv(SALES_FILE)

all_reviews = []
for shop in sales_df['coffeeshop_name'].unique():
    shop_reviews = reviews_df[reviews_df['coffeeshop_name'] == shop] if reviews_df is not None else None
    
    if shop_reviews is not None and not shop_reviews.empty:
        filled_reviews = shop_reviews.apply(fill_missing_values, axis=1)
        all_reviews.extend(filled_reviews.to_dict('records'))
    
    current_count = len(shop_reviews) if shop_reviews is not None else 0
    additional_needed = max(0, random.randint(30, 40) - current_count)
    
    for _ in range(additional_needed):
        review_data = generate_review()
        all_reviews.append({
            'coffeeshop_name': shop,
            'coffeeshop_url': generate_url(shop),
            **review_data
        })

column_order = ['coffeeshop_name', 'coffeeshop_url', 'rating', 'title', 'content', 'ReviewType']
merged_df = pd.DataFrame(all_reviews)[column_order]

merged_df.to_csv(OUTPUT_FILE, index=False)

review_counts = merged_df['coffeeshop_name'].value_counts()
print(f"Successfully processed {len(merged_df)} reviews for {len(review_counts)} coffee shops")
print("Review count per coffee shop:")
print(review_counts)
print("Review type distribution:")
print(merged_df['ReviewType'].value_counts())
print(f"Saved to: {OUTPUT_FILE}")