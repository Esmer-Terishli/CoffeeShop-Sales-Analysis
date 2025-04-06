# import pandas as pd

# file_path = r"C:\Users\ASUS\Desktop\CoffeeShop Sales Analysis\Data\raw\coffeeshop_sales.csv"
# df = pd.read_csv(file_path)

# new_column_names = [
#     "coffeeshop_name", "branch", "has_other_branches", "branch_locations", "most_popular_branch",
#     "peak_hours", "busiest_days", "peak_season", "best_weather_for_visits", "best_selling_product",
#     "least_selling_product", "avg_time_spent", "dominant_age_group", "new_vs_loyal_customers", "visit_purpose",
#     "solo_vs_group_visits", "customer_reaction_to_discounts", "recent_campaign_types", 
#     "products_in_campaigns", "sales_difference_after_campaigns", "preferred_payment_method",
#     "avg_order_price", "wolt_vs_inhouse_orders", "most_preferred_size", "seating_capacity",
#     "holiday_customer_increase", "has_loyalty_card", "winter_weekday_orders", "winter_weekend_orders",
#     "summer_weekday_orders", "summer_weekend_orders", "has_dietary_options", "americano_price",
#     "latte_price", "espresso_price", "cappuccino_price", "rafcoffee_price", "whitemocha_price",
#     "blackmocha_price", "hotchocolate_price", "tea_price"
# ]

# df.columns = new_column_names
# df.to_csv(file_path, index=False)
# print("✅ CSV column names updated and saved to:", file_path)




import pandas as pd

# CSV fayl yolunu göstər
file_path = r"C:\Users\ASUS\Desktop\CoffeeShop Sales Analysis\Data\raw\coffeeshop_sales.csv"

# CSV faylını oxu
df = pd.read_csv(file_path)

# 1. "branch yoxdur" olan sətirləri çıxart
df = df[df["branch"] != "branch yoxdur"]

# 2. branch_name sütununu yarad: coffeeshop_name + "-" + branch
df["branch_name"] = df["coffeeshop_name"] + "-" + df["branch"].str.strip()

# 3. Nəticəni seç: yalnız tələb olunan sütunlar
result = df[["coffeeshop_name", "branch", "branch_name"]]

# 4. Nəticəni göstər
print(result)

# 5. CSV faylına yaz
output_path = r"C:\Users\ASUS\Desktop\CoffeeShop Sales Analysis\Data\processed\bb3.csv"
result.to_csv(output_path, index=False)

print(f"\nNəticə {output_path} faylına yazıldı!")
