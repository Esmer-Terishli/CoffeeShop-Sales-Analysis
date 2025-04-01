import pandas as pd
import random

df = pd.read_csv("tripadvisor_scraping.csv")
df["Phone"] = df["Phone"].replace(["N/A", "n/a", "NA", "na", "", "None", "none"], pd.NA)
df["Phone"] = df["Phone"].fillna("Unknown")
df["Rating"] = [round(random.uniform(1, 5), 1) for _ in range(len(df))]
df["Review count"] = [random.randint(15, 101) for _ in range(len(df))]

def distribute_reviews(total):
    parts = [random.random() for _ in range(5)]
    total_parts = sum(parts)
    reviews = [int(total * p/total_parts) for p in parts]
    reviews[-1] = total - sum(reviews[:-1])
    return reviews

review_columns = [
    "Excellent Reviews", "Good Reviews", "Average Reviews",
    "Poor Reviews", "Terrible Reviews"
]

for index, row in df.iterrows():
    reviews = distribute_reviews(row["Review count"])
    for i, col in enumerate(review_columns):
        df.at[index, col] = max(0, reviews[i])

for col in review_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')

columns_to_check = [
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

for col in columns_to_check:
    if col in df.columns:
        df[col] = df[col].astype(str).str.lower().map({
            'true': 1, 'yes': 1, '1': 1,
            'false': 0, 'no': 0, '0': 0
        }).fillna(0).astype('int8')

columns_to_drop = [col for col in columns_to_check 
                  if col in df.columns and (df[col] == 0).all()]

if columns_to_drop:
    print(f"Dropping unused features: {columns_to_drop}")
    df = df.drop(columns=columns_to_drop)

df.to_csv("tripadvisor.csv", index=False)

print("PROCESSING COMPLETE")
print(df.dtypes)