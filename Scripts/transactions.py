import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta, date

fake = Faker()

transaction_data = []
num_rows = 200000

year_distribution = {
    2022: 0.20,
    2023: 0.25,
    2024: 0.45,
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
    'winter': 30,
    'spring': 12,
    'autumn': 8
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
    else:  # morning
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

priority_branches = [1, 48, 62, 23, 65, 55, 66, 34, 49, 56, 17, 29, 81, 21, 27, 22, 9,
                     25, 58, 20, 3, 73, 30, 45, 16, 33, 28, 64, 46, 2, 26, 54, 19, 59,
                     75, 36, 47]

year_counts = {year: int(num_rows * proportion) for year, proportion in year_distribution.items()}

for year, count in year_counts.items():
    for _ in range(count):
        transaction_date, season = generate_date_for_year(year)
        transaction_time, shift = generate_time_by_slot()

        transaction_qty = random.choices(
            population=[1, 2, 3, 4, 5, 6, 7, 8],
            weights=[30, 25, 20, 5, 5, 5, 5, 5],
            k=1
        )[0]

        branch_id = random.choices(
            population=priority_branches + list(set(range(1, 84)) - set(priority_branches)),
            weights=[1.7] * len(priority_branches) + [1] * (83 - len(priority_branches)),
            k=1
        )[0]

        isflagwolt = random.choices(['NO', 'YES'], weights=[90, 10], k=1)[0]

        product_id = random.randint(1, 9)

        transaction_data.append([ 
            transaction_date,
            transaction_time,
            transaction_qty,
            branch_id,
            product_id,
            isflagwolt,
            shift,
            season
        ])

columns = ['transaction_date', 'transaction_time', 'transaction_qty', 'branch_id', 'product_id', 'isflagwolt', 'shift', 'season']
df = pd.DataFrame(transaction_data, columns=columns)

df['datetime'] = pd.to_datetime(df['transaction_date'].astype(str) + ' ' + df['transaction_time'])
df_sorted = df.sort_values(by='datetime')
df_sorted = df_sorted.drop(columns=['datetime'])
df_unique = df_sorted.drop_duplicates(subset=['transaction_date', 'transaction_qty', 'branch_id', 'product_id', 'isflagwolt', 'shift', 'season'])
df_unique.to_csv('C:/Users/ASUS/Desktop/CoffeeShop Sales Analysis/Data/processed/transactions.csv', index=False)

print("Unique records have been written to the CSV file!")