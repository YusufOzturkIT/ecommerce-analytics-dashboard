

import sys
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import sqlite3

print("="*70)
print(" RUNNING SQL ANALYSIS QUERIES")


import pandas as pd
import sqlite3

print("="*70)
print(" RUNNING SQL ANALYSIS QUERIES")
print("="*70)


conn = sqlite3.connect('data/ecommerce.db')


print("\n" + "="*70)
print(" REVENUE BY CATEGORY")
print("="*70)

query1 = """
SELECT 
    category,
    COUNT(DISTINCT o.order_id) as total_orders,
    ROUND(SUM(oi.line_total), 2) as total_revenue,
    ROUND(AVG(oi.line_total), 2) as avg_item_value
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status != 'Cancelled'
GROUP BY category
ORDER BY total_revenue DESC
"""

df1 = pd.read_sql_query(query1, conn)
print("\n" + df1.to_string(index=False))



print("\n\n" + "="*70)
print(" TOP 10 CUSTOMERS BY LIFETIME VALUE")
print("="*70)

query2 = """
SELECT 
    c.first_name || ' ' || c.last_name as customer_name,
    c.country,
    COUNT(DISTINCT o.order_id) as total_orders,
    ROUND(SUM(o.final_amount), 2) as lifetime_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY lifetime_value DESC
LIMIT 10
"""

df2 = pd.read_sql_query(query2, conn)
print("\n" + df2.to_string(index=False))


print("\n\n" + "="*70)
print(" ORDERS BY STATUS")
print("="*70)

query3 = """
SELECT 
    order_status,
    COUNT(*) as order_count,
    ROUND(COUNT(*) * 100.0 / 2000, 1) as percentage
FROM orders
GROUP BY order_status
ORDER BY order_count DESC
"""

df3 = pd.read_sql_query(query3, conn)
print("\n" + df3.to_string(index=False))


print("\n\n" + "="*70)
print(" TOP 10 COUNTRIES BY ORDERS")
print("="*70)

query4 = """
SELECT 
    shipping_country as country,
    COUNT(*) as total_orders,
    ROUND(SUM(final_amount), 2) as total_revenue
FROM orders
GROUP BY shipping_country
ORDER BY total_orders DESC
LIMIT 10
"""

df4 = pd.read_sql_query(query4, conn)
print("\n" + df4.to_string(index=False))



print("\n\n" + "="*70)
print(" TOP 10 PRODUCTS BY REVENUE")
print("="*70)

query5 = """
SELECT 
    p.product_name,
    p.category,
    COUNT(oi.order_item_id) as units_sold,
    ROUND(SUM(oi.line_total), 2) as total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_revenue DESC
LIMIT 10
"""

df5 = pd.read_sql_query(query5, conn)
print("\n" + df5.to_string(index=False))


print("\n\n" + "="*70)
print(" KEY PERFORMANCE INDICATORS (KPIs)")
print("="*70)

cursor = conn.cursor()

cursor.execute("SELECT SUM(final_amount) FROM orders WHERE order_status != 'Cancelled'")
total_revenue = cursor.fetchone()[0]


cursor.execute("SELECT COUNT(*) FROM orders WHERE order_status != 'Cancelled'")
total_orders = cursor.fetchone()[0]


cursor.execute("SELECT COUNT(*) FROM customers")
total_customers = cursor.fetchone()[0]


cursor.execute("SELECT AVG(final_amount) FROM orders WHERE order_status != 'Cancelled'")
avg_order_value = cursor.fetchone()[0]


cursor.execute("SELECT COUNT(*) FROM orders WHERE order_status = 'Delivered'")
delivered = cursor.fetchone()[0]

print(f"\n Total Revenue:        ${total_revenue:,.2f}")
print(f" Total Orders:         {total_orders:,}")
print(f" Total Customers:      {total_customers:,}")
print(f" Avg Order Value:      ${avg_order_value:,.2f}")
print(f" Delivered Orders:     {delivered:,} ({(delivered/total_orders)*100:.1f}%)")
print(f" Customer Lifetime Value: ${total_revenue/total_customers:,.2f}")

conn.close()

print("\n" + "="*70)
print(" ANALYSIS COMPLETE!")
print("="*70)