import pandas as pd
import numpy as np

wolt_prices = pd.read_csv('C:/Users/ASUS/Desktop/CoffeeShop Sales Analysis/Data/processed/wolt_prices.csv')
coffeeshop_sales = pd.read_csv('C:/Users/ASUS/Desktop/CoffeeShop Sales Analysis/Data/raw/coffeeshop_sales.csv')

coffeeshop_sales['coffeeshop_name'] = coffeeshop_sales['coffeeshop_name'].str.strip().str.lower()
wolt_prices['CoffeeShop Name'] = wolt_prices['CoffeeShop Name'].str.strip().str.lower()

unique_wolt = wolt_prices.drop_duplicates(subset=['CoffeeShop Name']).copy()
unique_wolt = unique_wolt.rename(columns={'CoffeeShop Name': 'coffeeshop_name'})

merged_all = pd.merge(
    coffeeshop_sales[['coffeeshop_name']],
    unique_wolt,
    on='coffeeshop_name',
    how='left'
).drop_duplicates(subset=['coffeeshop_name']).reset_index(drop=True)


def generate_price_series(n, low_range, dense_range, dense_ratio=0.7):
    dense_count = int(n * dense_ratio)
    sparse_count = n - dense_count
    dense_part = np.random.uniform(dense_range[0], dense_range[1], dense_count)
    sparse_part = np.random.uniform(low_range[0], low_range[1], sparse_count)
    all_values = np.concatenate([dense_part, sparse_part])
    np.random.shuffle(all_values)
    return all_values.round(1)


missing_mask = merged_all['Americano Price'].isna()
missing_count = missing_mask.sum()

merged_all.loc[missing_mask, 'Americano Price'] = generate_price_series(missing_count, (6, 9), (8, 9))
merged_all.loc[missing_mask, 'Latte Price'] = generate_price_series(missing_count, (7, 9), (8, 9))
merged_all.loc[missing_mask, 'Espresso Price'] = generate_price_series(missing_count, (3.5, 9), (6, 9))
merged_all.loc[missing_mask, 'Cappuccino Price'] = generate_price_series(missing_count, (6, 9), (8, 9))
merged_all.loc[missing_mask, 'Raf Coffee Price'] = generate_price_series(missing_count, (7, 11), (9, 11))
merged_all.loc[missing_mask, 'White Mocha Price'] = generate_price_series(missing_count, (7, 11), (9, 11))
merged_all.loc[missing_mask, 'Black Mocha Price'] = generate_price_series(missing_count, (7, 11), (9, 11))
merged_all.loc[missing_mask, 'Hot Chocolate Price'] = generate_price_series(missing_count, (6.5, 11), (8, 11))
merged_all.loc[missing_mask, 'Tea Price'] = generate_price_series(missing_count, (4, 10), (6, 9))

merged_all.to_csv('C:/Users/ASUS/Desktop/CoffeeShop Sales Analysis/Data/processed/merged_coffeeshop_wolt.csv', index=False)
print(merged_all)