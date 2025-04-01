import pandas as pd

input_file = 'wolt_prices_scraping.csv'
df = pd.read_csv(input_file)

columns_to_check = [
    "Americano", "Latte", "Espresso", "Cappuccino", 
    "Raf Coffee", "White Mocha", "Black Mocha", "Hot Chocolate", "Tea"
]

df_cleaned = df.dropna(subset=columns_to_check, how='all').fillna(0)
df_cleaned[columns_to_check] = df_cleaned[columns_to_check].where(df_cleaned[columns_to_check] <= 10, 7)
df_cleaned[columns_to_check] = df_cleaned[columns_to_check].astype(int)
df_cleaned.columns = [col + " Price" if col != "CoffeeShop Name" else col for col in df_cleaned.columns]

print(df_cleaned.dtypes)

output_file = 'wolt_prices.csv'
df_cleaned.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"Cleaned data has been written to '{output_file}' file.")