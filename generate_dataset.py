import pandas as pd
import random
from datetime import datetime, timedelta
import csv

# Product catalog with realistic grocery items
products = {
    'P001': ('Bread', 2.99), 'P002': ('Milk', 3.49), 'P003': ('Eggs', 4.99), 'P004': ('Butter', 5.49), 'P005': ('Cheese', 6.99),
    'P006': ('Yogurt', 1.99), 'P007': ('Chicken', 8.99), 'P008': ('Beef', 12.99), 'P009': ('Fish', 9.99), 'P010': ('Rice', 3.99),
    'P011': ('Pasta', 2.49), 'P012': ('Tomatoes', 2.99), 'P013': ('Onions', 1.99), 'P014': ('Potatoes', 2.49), 'P015': ('Carrots', 1.79),
    'P016': ('Apples', 3.99), 'P017': ('Bananas', 1.99), 'P018': ('Oranges', 4.49), 'P019': ('Cereal', 4.99), 'P020': ('Coffee', 7.99),
    'P021': ('Tea', 3.99), 'P022': ('Sugar', 2.99), 'P023': ('Salt', 1.49), 'P024': ('Pepper', 2.99), 'P025': ('Oil', 4.99),
    'P026': ('Vinegar', 2.49), 'P027': ('Flour', 3.49), 'P028': ('Baking_Powder', 1.99), 'P029': ('Vanilla', 3.99), 'P030': ('Chocolate', 4.99),
    'P031': ('Ice_Cream', 5.99), 'P032': ('Frozen_Pizza', 6.99), 'P033': ('Soup', 2.99), 'P034': ('Crackers', 3.49), 'P035': ('Peanut_Butter', 4.99),
    'P036': ('Jam', 3.99), 'P037': ('Honey', 5.99), 'P038': ('Nuts', 6.99), 'P039': ('Chips', 3.99), 'P040': ('Soda', 2.99),
    'P041': ('Juice', 3.99), 'P042': ('Water', 1.99), 'P043': ('Beer', 8.99), 'P044': ('Wine', 12.99), 'P045': ('Detergent', 7.99),
    'P046': ('Shampoo', 5.99), 'P047': ('Toothpaste', 3.99), 'P048': ('Soap', 2.99), 'P049': ('Tissues', 4.99), 'P050': ('Paper_Towels', 6.99)
}

# Product associations for realistic patterns
associations = {
    'P001': ['P002', 'P004', 'P035', 'P036'],  # Bread with Milk, Butter, PB, Jam
    'P002': ['P001', 'P019', 'P020', 'P030'],  # Milk with Bread, Cereal, Coffee, Chocolate
    'P003': ['P001', 'P004', 'P027'],          # Eggs with Bread, Butter, Flour
    'P007': ['P010', 'P012', 'P014'],          # Chicken with Rice, Tomatoes, Potatoes
    'P008': ['P010', 'P013', 'P014'],          # Beef with Rice, Onions, Potatoes
    'P019': ['P002', 'P017'],                  # Cereal with Milk, Bananas
    'P020': ['P002', 'P022'],                  # Coffee with Milk, Sugar
    'P032': ['P040', 'P043'],                  # Pizza with Soda, Beer
    'P039': ['P040', 'P043'],                  # Chips with Soda, Beer
    'P045': ['P046', 'P047', 'P048']           # Detergent with Shampoo, Toothpaste, Soap
}

stores = ['STORE01', 'STORE02', 'STORE03', 'STORE04', 'STORE05']
customers = [f'CUST{i:03d}' for i in range(1, 501)]

def generate_transaction_items(transaction_id):
    """Generate 2-5 items for a transaction with realistic associations"""
    num_items = random.randint(2, 5)
    selected_items = set()
    
    # Start with a random item
    first_item = random.choice(list(products.keys()))
    selected_items.add(first_item)
    
    # Add associated items with higher probability
    for _ in range(num_items - 1):
        if len(selected_items) >= num_items:
            break
            
        # 60% chance to add associated item, 40% random
        if random.random() < 0.6 and first_item in associations:
            candidates = [item for item in associations[first_item] if item not in selected_items]
            if candidates:
                selected_items.add(random.choice(candidates))
                continue
        
        # Add random item
        available_items = [item for item in products.keys() if item not in selected_items]
        if available_items:
            selected_items.add(random.choice(available_items))
    
    return list(selected_items)

# Generate dataset
data = []
start_date = datetime(2024, 1, 1)
transaction_id = 1001

for _ in range(1500):
    # Generate transaction details
    trans_id = f'T{transaction_id}'
    date = start_date + timedelta(days=random.randint(0, 89))
    time = f'{random.randint(8, 21):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}'
    customer = random.choice(customers)
    store = random.choice(stores)
    
    # Generate items for this transaction
    items = generate_transaction_items(trans_id)
    
    # Create rows for each item
    for item_id in items:
        item_name, base_price = products[item_id]
        quantity = random.randint(1, 5)
        price = round(base_price * random.uniform(0.9, 1.1), 2)
        
        data.append([
            trans_id,
            date.strftime('%Y-%m-%d'),
            time,
            customer,
            item_id,
            item_name,
            quantity,
            price,
            store
        ])
    
    transaction_id += 1

# Create DataFrame and save to CSV
df = pd.DataFrame(data, columns=[
    'Transaction_ID', 'Date_of_Purchase', 'Time_of_Purchase', 
    'Customer_ID', 'Item_ID', 'Item_Name', 'Quantity', 'Price', 'Store_ID'
])

# Save to CSV
output_path = 'market_basket_dataset.csv'
df.to_csv(output_path, index=False)

print(f"Dataset generated successfully!")
print(f"Total transactions: {len(df['Transaction_ID'].unique())}")
print(f"Total records: {len(df)}")
print(f"Unique products: {len(df['Item_ID'].unique())}")
print(f"Unique customers: {len(df['Customer_ID'].unique())}")
print(f"Date range: {df['Date_of_Purchase'].min()} to {df['Date_of_Purchase'].max()}")