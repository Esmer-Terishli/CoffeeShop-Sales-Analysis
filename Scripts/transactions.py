# import pandas as pd
# from faker import Faker
# import random
# from datetime import datetime, timedelta

# # Faker obyektini yaratmaq
# fake = Faker()

# # Nümunə məlumatlar
# transaction_data = []

# # Məlumatın sayını təyin edirik (misal üçün 1000)
# for _ in range(1000):
#     transaction_id = fake.unique.random_int(min=1, max=1000000)
#     transaction_date = fake.date_this_decade()
#     transaction_time = fake.time()
#     transaction_qty = random.randint(1, 10)  # 1-10 arasında təsadüfi sayda məhsul
#     branch_id = random.randint(1, 10)  # branch_id sayını uyğunlaşdırın
#     product_id = random.randint(1, 100)  # product_id sayını uyğunlaşdırın
#     isflagwolt = random.choice(['YES', 'NO'])
    
#     transaction_data.append([
#         transaction_id,
#         transaction_date,
#         transaction_time,
#         transaction_qty,
#         branch_id,
#         product_id,
#         isflagwolt
#     ])

# # DataFrame yaratmaq
# columns = ['transaction_id', 'transaction_date', 'transaction_time', 'transaction_qty', 'branch_id', 'product_id', 'isflagwolt']
# df = pd.DataFrame(transaction_data, columns=columns)

# # CSV faylına yazmaq
# df.to_csv('xxxxx.csv', index=False)

# print("CSV faylına məlumatlar əlavə edildi!")



import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta, date

fake = Faker()

transaction_data = []
num_rows = 10000
transaction_ids = random.sample(range(1, num_rows + 1), num_rows)

# İllərə görə satış faiz bölgüsü (təxmini olaraq): 2022-40%, 2023-60%, 2024-80%, 2025-in ilk 3 ayı az faiz
year_distribution = {
    2022: 0.20,
    2023: 0.25,
    2024: 0.45,
    2025: 0.10
}

# Hər il üçün neçə sətir düşəcəyini hesablayaq
year_counts = {year: int(num_rows * proportion) for year, proportion in year_distribution.items()}

# Prioritet branch-lar
priority_branches = [1, 48, 62, 23, 65, 55, 66, 34, 49, 56, 17, 29, 81, 21, 27, 22, 9,
                     25, 58, 20, 3, 73, 30, 45, 16, 33, 28, 64, 46, 2, 26, 54, 19, 59,
                     75, 36, 47]

def generate_date_for_year(year):
    if year == 2025:
        start = date(2025, 1, 1)
        end = date(2025, 3, 31)
    else:
        start = date(year, 1, 1)
        end = date(year, 12, 31)
    return fake.date_between(start_date=start, end_date=end)

for year, count in year_counts.items():
    for _ in range(count):
        transaction_id = transaction_ids.pop()
        transaction_date = generate_date_for_year(year)
        transaction_time = fake.time()

        transaction_qty = random.choices(
            population=[1, 2, 3, 4, 5, 6, 7, 8],
            weights=[20, 20, 20, 20, 5, 5, 5, 5],
            k=1
        )[0]

        # 70% ehtimalla prioritet filial seçilir
        branch_id = random.choices(
            population=priority_branches + list(set(range(1, 84)) - set(priority_branches)),
            weights=[1.7] * len(priority_branches) + [1] * (83 - len(priority_branches)),
            k=1
        )[0]

        # 90% ehtimalla isflagwolt = NO
        isflagwolt = random.choices(['NO', 'YES'], weights=[90, 10], k=1)[0]

        product_id = random.randint(1, 9)

        transaction_data.append([
            transaction_id,
            transaction_date,
            transaction_time,
            transaction_qty,
            branch_id,
            product_id,
            isflagwolt
        ])

# DataFrame
columns = ['transaction_id', 'transaction_date', 'transaction_time', 'transaction_qty', 'branch_id', 'product_id', 'isflagwolt']
df = pd.DataFrame(transaction_data, columns=columns)

# CSV faylına yaz
df.to_csv('C:/Users/ASUS/Desktop/CoffeeShop Sales Analysis/Data/processed/transactions.csv', index=False)
print("CSV faylına 10,000 məlumat əlavə edildi!")

