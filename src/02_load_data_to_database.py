

import pandas as pd
import sqlite3
from pathlib import Path

print("="*70)
print(" LOADING DATA TO SQLITE DATABASE")
print("="*70)



db_path = 'data/ecommerce.db'

print(f"\n Connecting to database: {db_path}")


conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("    Connected to SQLite database")


print("\n Creating tables...")


with open('sql/01_create_tables.sql', 'r') as f:
    sql_script = f.read()


cursor.executescript(sql_script)
conn.commit()

print("    All tables created successfully")


files_to_load = [
    ('data/raw/customers.csv', 'customers'),
    ('data/raw/products.csv', 'products'),
    ('data/raw/orders.csv', 'orders'),
    ('data/raw/order_items.csv', 'order_items'),
]

print("\n Loading CSV files into database...\n")

for csv_file, table_name in files_to_load:
    
    print(f"   Loading {csv_file}...")
    
   
    if not Path(csv_file).exists():
        print(f"    ERROR: File not found - {csv_file}")
        continue
    
 
    df = pd.read_csv(csv_file)
  
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
  
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"       Loaded {len(df):,} rows into {table_name}")
    except Exception as e:
        print(f"       Error loading {table_name}: {str(e)}")



print("\n VERIFYING DATA IN DATABASE:\n")

tables = ['customers', 'products', 'orders', 'order_items']

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"   {table:15} → {count:,} rows")



print("\n SAMPLE DATA FROM EACH TABLE:\n")

print("   CUSTOMERS (first 3 rows):")
print("   " + "-"*65)
df_customers = pd.read_sql_query("SELECT * FROM customers LIMIT 3", conn)
print(df_customers.to_string(index=False))

print("\n\n   PRODUCTS (first 3 rows):")
print("   " + "-"*65)
df_products = pd.read_sql_query("SELECT * FROM products LIMIT 3", conn)
print(df_products.to_string(index=False))

print("\n\n   ORDERS (first 3 rows):")
print("   " + "-"*65)
df_orders = pd.read_sql_query("SELECT * FROM orders LIMIT 3", conn)
print(df_orders.to_string(index=False))

print("\n\n   ORDER_ITEMS (first 3 rows):")
print("   " + "-"*65)
df_order_items = pd.read_sql_query("SELECT * FROM order_items LIMIT 3", conn)
print(df_order_items.to_string(index=False))



print("\n" + "="*70)
print(" DATABASE STATISTICS")
print("="*70)


cursor.execute("SELECT SUM(final_amount) FROM orders")
total_revenue = cursor.fetchone()[0]


cursor.execute("SELECT AVG(final_amount) FROM orders")
avg_order_value = cursor.fetchone()[0]


cursor.execute("""
    SELECT order_status, COUNT(*) as count
    FROM orders
    GROUP BY order_status
    ORDER BY count DESC
""")
status_counts = cursor.fetchall()


cursor.execute("""
    SELECT shipping_country, COUNT(*) as orders
    FROM orders
    GROUP BY shipping_country
    ORDER BY orders DESC
    LIMIT 3
""")
top_countries = cursor.fetchall()


cursor.execute("""
    SELECT 
        p.category,
        COUNT(o.order_id) as order_count,
        SUM(oi.line_total) as revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    GROUP BY p.category
    ORDER BY revenue DESC
    LIMIT 3
""")
top_categories = cursor.fetchall()

print(f"\n REVENUE:")
print(f"   Total Revenue: ${total_revenue:,.2f}")
print(f"   Average Order Value: ${avg_order_value:,.2f}")

print(f"\n ORDERS BY STATUS:")
for status, count in status_counts:
    percentage = (count / 2000) * 100
    print(f"   {status:15} → {count:4} orders ({percentage:5.1f}%)")

print(f"\n TOP COUNTRIES:")
for country, count in top_countries:
    print(f"   {country:15} → {count:4} orders")

print(f"\n TOP CATEGORIES BY REVENUE:")
for category, count, revenue in top_categories:
    print(f"   {category:20} → {count:3} orders, ${revenue:,.2f}")


conn.close()

print("\n" + "="*70)
print(" DATA LOADING COMPLETE!")
print("="*70)
print(f"\n Database location: {db_path}")
print("   Ready for SQL analysis! \n")