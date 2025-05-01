import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta, date

fake = Faker()

transaction_data = []
num_rows = 2000000

year_distribution = {
    2020: 0.05,
    2021: 0.10,
    2022: 0.15,
    2023: 0.20,
    2024: 0.40,
    2025: 0.10
}

season_distribution = {
    'summer': (6, 7, 8),
    'winter': (12, 1, 2),
    'spring': (3, 4, 5),
    'autumn': (9, 10, 11)
}
season_weights = {
    'summer': 50,
    'winter': 20,
    'spring': 15,
    'autumn': 15
}

def generate_time_by_slot():
    shift = random.choices(
        population=["evening", "afternoon", "morning"],
        weights=[50, 35, 15],
        k=1
    )[0]

    if shift == "evening":
        hour = random.randint(16, 21)
    elif shift == "afternoon":
        hour = random.randint(12, 15)
    else:
        hour = random.randint(8, 11)

    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
    return time_str, shift

def pick_month_by_season():
    season = random.choices(
        population=list(season_weights.keys()),
        weights=list(season_weights.values()),
        k=1
    )[0]
    return random.choice(season_distribution[season]), season

def generate_date_for_year(year):
    while True:
        month, season = pick_month_by_season()
        if year == 2025 and month > 3:
            continue
        if month == 2:
            day = random.randint(1, 28)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 31)
        try:
            return date(year, month, day), season
        except:
            continue

def generate_normalized_weights(ranges):
    raw_weights = [random.randint(r[0], r[1]) for r in ranges]
    total = sum(raw_weights)
    normalized = [round((w / total) * 100, 2) for w in raw_weights]

    diff = round(100 - sum(normalized), 2)
    if diff != 0:
        max_index = normalized.index(max(normalized))
        normalized[max_index] = round(normalized[max_index] + diff, 2)

    return normalized

group_15 = [9, 10, 14, 17, 33, 34, 43, 44, 59, 62, 66, 67, 69, 81]
group_30 = [26, 27, 37, 46, 49, 50, 52, 57, 65, 72, 73, 75, 83]
group_55 = [6, 18, 19, 20, 21, 28, 29, 32, 47, 48, 55, 60, 63, 70]

branch_weights = {}
for bid in group_15:
    branch_weights[bid] = 15
for bid in group_30:
    branch_weights[bid] = 30
for bid in group_55:
    branch_weights[bid] = 55

all_branches = list(range(1, 84))
for bid in all_branches:
    if bid not in branch_weights:
        branch_weights[bid] = random.randint(7, 12)

branch_population = list(branch_weights.keys())
branch_weight_values = list(branch_weights.values())

product_weight_ranges = [(25, 30), (25, 30), (7, 12), (4, 11), (2, 5), (2, 9), (1, 4), (1, 7), (1, 3)]
product_weights = generate_normalized_weights(product_weight_ranges)

year_counts = {year: int(num_rows * proportion) for year, proportion in year_distribution.items()}

# İstədiyin yeni tələblərlə:
weekday_branches = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,50,60,61,62,63,64,76,77,78,79,80,81,82,83]
weekend_branches = [27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,51,52,53,54,55,56,57,58,59,65,66,67,68,69,70,71,72,73,74,75]

for year, count in year_counts.items():
    for _ in range(count):
        transaction_date, season = generate_date_for_year(year)
        transaction_time, shift = generate_time_by_slot()

        weekday_idx = transaction_date.weekday()
        is_weekend = weekday_idx >= 5

        follow_rule = random.choices([True, False], weights=[random.randint(60, 70), random.randint(30, 40)], k=1)[0]

        if follow_rule:
            branch_candidates = weekend_branches if is_weekend else weekday_branches
        else:
            branch_candidates = weekday_branches if is_weekend else weekend_branches

        branch_id = random.choice(branch_candidates)

        transaction_qty = random.choices(
            population=[1, 2, 3, 4, 5, 6, 7, 8],
            weights=[30, 25, 20, 5, 5, 5, 5, 5],
            k=1
        )[0]

        isflagwolt = random.choices(['NO', 'YES'], weights=[90, 10], k=1)[0]

        product_id = random.choices(
            population=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            weights=product_weights,
            k=1
        )[0]

        transaction_data.append([transaction_date, transaction_time, transaction_qty, branch_id, product_id, isflagwolt, shift, season])

columns = ['transaction_date', 'transaction_time', 'transaction_qty', 'branch_id', 'product_id', 'isflagwolt', 'shift', 'season']
df = pd.DataFrame(transaction_data, columns=columns)

df['datetime'] = pd.to_datetime(df['transaction_date'].astype(str) + ' ' + df['transaction_time'])
df_sorted = df.sort_values(by='datetime')
df_sorted = df_sorted.drop(columns=['datetime'])
df_unique = df_sorted.drop_duplicates(subset=['transaction_date', 'transaction_qty', 'branch_id', 'product_id', 'isflagwolt', 'shift', 'season'])
df_unique.to_csv('C:/Users/ASUS/Desktop/CoffeeShop Sales Analysis/Data/processed/transactions.csv', index=False)

print("Unique records have been written to the CSV file!")