"""
E-Commerce Sample Data Generator
Purpose: Generate realistic e-commerce data for analytics
Output: CSV files for database import
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


np.random.seed(42)
random.seed(42)

print("="*70)
print(" GENERATING E-COMMERCE SAMPLE DATA")
print("="*70)


print("\n Generating CUSTOMERS data...")

n_customers = 500

first_names = [
    'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emma', 'Robert', 'Lisa',
    'James', 'Mary', 'William', 'Patricia', 'Richard', 'Jennifer', 'Thomas'
]

last_names = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
    'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez'
]

countries = ['USA', 'UK', 'Germany', 'France', 'Spain', 'Poland', 'Netherlands', 'Canada']

cities = {
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston'],
    'UK': ['London', 'Manchester', 'Liverpool'],
    'Germany': ['Berlin', 'Munich', 'Hamburg'],
    'France': ['Paris', 'Lyon', 'Marseille'],
    'Spain': ['Madrid', 'Barcelona', 'Valencia'],
    'Poland': ['Warsaw', 'Krakow', 'Wroclaw'],
    'Netherlands': ['Amsterdam', 'Rotterdam', 'The Hague'],
    'Canada': ['Toronto', 'Vancouver', 'Montreal']
}

customers_data = {
    'customer_id': range(1001, 1001 + n_customers),
    'first_name': [random.choice(first_names) for _ in range(n_customers)],
    'last_name': [random.choice(last_names) for _ in range(n_customers)],
    'country': [random.choice(countries) for _ in range(n_customers)],
}


customers_data['city'] = [
    random.choice(cities[country]) 
    for country in customers_data['country']
]


customers_data['email'] = [
    f"{first.lower()}.{last.lower()}_{i}@email.com"
    for i, (first, last) in enumerate(
        zip(customers_data['first_name'], customers_data['last_name'])
    )
]


customers_data['registration_date'] = [
    (datetime(2022, 1, 1) + timedelta(days=int(x))).date()
    for x in np.random.randint(0, 730, n_customers)
]

customers_df = pd.DataFrame(customers_data)

print(f"    Created {len(customers_df)} customers")
print(f"      Sample: {customers_df.head(2).to_string(index=False)}")


print("\n Generating PRODUCTS data...")

n_products = 100

categories = {
    'Electronics': ['Laptops', 'Smartphones', 'Tablets'],
    'Clothing': ['Men', 'Women', 'Kids'],
    'Home & Garden': ['Furniture', 'Decor', 'Kitchen'],
    'Books': ['Fiction', 'Non-Fiction', 'Science'],
    'Sports': ['Equipment', 'Apparel', 'Shoes']
}

products_data = {
    'product_id': range(2001, 2001 + n_products),
    'product_name': [],
    'category': [],
    'subcategory': [],
    'unit_price': [],
    'cost_price': [],
}

product_names_base = [
    'Premium', 'Standard', 'Deluxe', 'Professional', 'Compact', 'Ultra', 'Smart'
]
product_types = [
    'Device', 'Product', 'Item', 'Set', 'Kit', 'Bundle'
]

for _ in range(n_products):
    category = random.choice(list(categories.keys()))
    subcategory = random.choice(categories[category])
    
    name = f"{random.choice(product_names_base)} {subcategory} {random.choice(product_types)}"
    
    products_data['category'].append(category)
    products_data['subcategory'].append(subcategory)
    products_data['product_name'].append(name)
    
   
    if category == 'Electronics':
        price = np.random.uniform(500, 2000)
    elif category == 'Clothing':
        price = np.random.uniform(30, 150)
    elif category == 'Books':
        price = np.random.uniform(10, 50)
    else:
        price = np.random.uniform(20, 500)
    
    unit_price = round(price, 2)
    cost_price = round(unit_price * np.random.uniform(0.4, 0.7), 2)
    
    products_data['unit_price'].append(unit_price)
    products_data['cost_price'].append(cost_price)

products_data['stock_quantity'] = np.random.randint(10, 1000, n_products)

products_data['is_active'] = np.random.choice(
    [True, False], 
    n_products, 
    p=[0.9, 0.1]
)

products_df = pd.DataFrame(products_data)

print(f"    Created {len(products_df)} products")
print(f"      Sample: {products_df.head(2).to_string(index=False)}")



print("\n Generating ORDERS data...")

n_orders = 2000

order_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Returned']
payment_methods = ['Credit Card', 'PayPal', 'Bank Transfer', 'Debit Card']

orders_data = {
    'order_id': range(3001, 3001 + n_orders),
    'customer_id': np.random.choice(customers_df['customer_id'], n_orders),
    'order_date': [],
    'ship_date': [],
    'delivery_date': [],
    'total_amount': np.random.uniform(50, 1000, n_orders),
    'discount_amount': [],
    'order_status': np.random.choice(order_statuses, n_orders, p=[0.1, 0.2, 0.3, 0.25, 0.1, 0.05]),
    'payment_method': np.random.choice(payment_methods, n_orders),
}


base_date = datetime(2023, 1, 1)
for _ in range(n_orders):
    order_date = (base_date + timedelta(days=int(np.random.randint(0, 730)))).date()
    orders_data['order_date'].append(order_date)
    
   
    ship_date = order_date + timedelta(days=np.random.randint(1, 4))
    orders_data['ship_date'].append(ship_date)
    
    
    delivery_date = ship_date + timedelta(days=np.random.randint(5, 15))
    orders_data['delivery_date'].append(delivery_date)


orders_data['discount_amount'] = [
    round(total * np.random.uniform(0, 0.2), 2)
    for total in orders_data['total_amount']
]


orders_data['final_amount'] = [
    round(total - discount, 2)
    for total, discount in zip(orders_data['total_amount'], orders_data['discount_amount'])
]


orders_data['shipping_country'] = [
    customers_df[customers_df['customer_id'] == cid]['country'].values[0]
    for cid in orders_data['customer_id']
]

orders_df = pd.DataFrame(orders_data)

print(f"    Created {len(orders_df)} orders")
print(f"      Sample: {orders_df.head(2).to_string(index=False)}")



print("\n Generating ORDER_ITEMS data...")

order_items_data = {
    'order_item_id': [],
    'order_id': [],
    'product_id': [],
    'quantity': [],
    'unit_price': [],
    'line_total': [],
    'discount_percent': [],
}

item_id = 4001
items_per_order = np.random.poisson(2, n_orders) + 1 

for order_id, n_items in zip(orders_data['order_id'], items_per_order):
    for _ in range(max(1, n_items)): 
        product = products_df.sample(1).iloc[0]
        quantity = np.random.randint(1, 5)
        unit_price = product['unit_price']
        discount_percent = np.random.choice([0, 5, 10, 15, 20], p=[0.5, 0.2, 0.15, 0.1, 0.05])
        
        line_total = quantity * unit_price * (1 - discount_percent/100)
        
        order_items_data['order_item_id'].append(item_id)
        order_items_data['order_id'].append(order_id)
        order_items_data['product_id'].append(product['product_id'])
        order_items_data['quantity'].append(quantity)
        order_items_data['unit_price'].append(unit_price)
        order_items_data['line_total'].append(round(line_total, 2))
        order_items_data['discount_percent'].append(discount_percent)
        
        item_id += 1

order_items_df = pd.DataFrame(order_items_data)

print(f"    Created {len(order_items_df)} order items")
print(f"      Sample: {order_items_df.head(2).to_string(index=False)}")



print("\n SAVING TO CSV FILES...\n")

customers_df.to_csv('data/raw/customers.csv', index=False)
print(f"    Saved: data/raw/customers.csv ({len(customers_df)} rows)")

products_df.to_csv('data/raw/products.csv', index=False)
print(f"    Saved: data/raw/products.csv ({len(products_df)} rows)")

orders_df.to_csv('data/raw/orders.csv', index=False)
print(f"   Saved: data/raw/orders.csv ({len(orders_df)} rows)")

order_items_df.to_csv('data/raw/order_items.csv', index=False)
print(f"    Saved: data/raw/order_items.csv ({len(order_items_df)} rows)")



print("\n" + "="*70)
print(" DATA GENERATION COMPLETE!")
print("="*70)

print(f"\n Summary:")
print(f"   Total Customers: {len(customers_df):,}")
print(f"   Total Products: {len(products_df):,}")
print(f"   Total Orders: {len(orders_df):,}")
print(f"   Total Order Items: {len(order_items_df):,}")

print(f"\n Revenue Statistics:")
print(f"   Total Revenue: ${orders_df['final_amount'].sum():,.2f}")
print(f"   Average Order Value: ${orders_df['final_amount'].mean():,.2f}")
print(f"   Median Order Value: ${orders_df['final_amount'].median():,.2f}")

print(f"\n CSV files ready in: data/raw/")
print(f"   Next step: Load into database\n")