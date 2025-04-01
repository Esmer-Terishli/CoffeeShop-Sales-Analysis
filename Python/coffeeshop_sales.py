import pandas as pd

df = pd.read_csv("coffeeshop_sales.csv")

new_column_names = [
    "coffeeshop_name", "branch", "has_other_branches", "branch_locations", "most_popular_branch",
    "peak_hours", "busiest_days", "peak_season", "best_weather_for_visits", "best_selling_product",
    "least_selling_product", "avg_time_spent", "dominant_age_group", "new_vs_loyal_customers", "visit_purpose",
    "solo_vs_group_visits", "customer_reaction_to_discounts", "recent_campaign_types", 
    "products_in_campaigns", "sales_difference_after_campaigns", "preferred_payment_method",
    "avg_order_price", "wolt_vs_inhouse_orders", "most_preferred_size", "seating_capacity",
    "holiday_customer_increase", "has_loyalty_card", "winter_weekday_orders", "winter_weekend_orders",
    "summer_weekday_orders", "summer_weekend_orders", "has_dietary_options", "americano_price",
    "latte_price", "espresso_price", "cappuccino_price", "rafcoffee_price", "whitemocha_price",
    "blackmocha_price", "hotchocolate_price", "tea_price"
]

df.columns = new_column_names
df.to_csv("coffeeshop_sales.csv", index=False)
print("CSV column names updated and saved to 'coffeeshop_sales.csv'.")