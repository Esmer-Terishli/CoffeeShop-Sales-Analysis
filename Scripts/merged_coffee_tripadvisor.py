import pandas as pd
import random
import numpy as np

sales_path = r"C:\Users\ASUS\Desktop\CoffeeShop Sales Analysis\Data\raw\coffeeshop_sales.csv"
tripadvisor_path = r"C:\Users\ASUS\Desktop\CoffeeShop Sales Analysis\Data\processed\tripadvisor.csv"
output_path = r"C:\Users\ASUS\Desktop\CoffeeShop Sales Analysis\Data\processed\merged_coffeeshop_tripadvisor.csv"

sales_df = pd.read_csv(sales_path)
tripadvisor_df = pd.read_csv(tripadvisor_path)

tripadvisor_df = tripadvisor_df.drop(columns=['URL', 'Address'])
merged_df = sales_df.merge(tripadvisor_df, left_on="coffeeshop_name", right_on="CoffeeShop Name", how="left")

def random_phone():
    prefixes = ["+994 50", "+994 55", "+994 12"]
    return f"{random.choice(prefixes)} {random.randint(100,999)} {random.randint(10,99)} {random.randint(10,99)}"

merged_df['Phone'] = merged_df['Phone'].apply(lambda x: random_phone() if pd.isnull(x) else x)

merged_df['Rating'] = merged_df['Rating'].apply(lambda x: round(random.uniform(1.0, 5.0), 1) if pd.isnull(x) else x)

def random_review_count():
    return random.randint(30, 120)

merged_df['Review count'] = merged_df['Review count'].apply(lambda x: random_review_count() if pd.isnull(x) else x)
review_cols = ['Excellent Reviews', 'Good Reviews', 'Average Reviews', 'Poor Reviews', 'Terrible Reviews']

def split_reviews(total):
    parts = np.random.multinomial(total, [0.3, 0.25, 0.2, 0.15, 0.1])
    return parts

for i, row in merged_df.iterrows():
    if any(pd.isnull(row[col]) for col in review_cols):
        total = row['Review count']
        parts = split_reviews(total)
        for col, val in zip(review_cols, parts):
            merged_df.at[i, col] = val

service_cols = [
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

for col in service_cols:
    if col == "Beach" or col == "Wine and Beer":
        merged_df[col] = merged_df[col].fillna(0)
    else:
        merged_df[col] = merged_df[col].apply(lambda x: 1 if pd.isnull(x) and random.random() < 0.1 else (0 if pd.isnull(x) else x))

merged_df.to_csv(output_path, index=False)
print("✅ CSV file successfully created:", output_path)
