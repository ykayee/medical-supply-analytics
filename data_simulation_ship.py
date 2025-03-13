#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


# In[8]:


df_item = pd.read_csv('item.csv')
df_item.head()


# In[30]:


#Customer table

customers = [
    "CareFirst Home Health", "BrightPath Senior Services", "SafeHaven Care Solutions",
    "GentleHands Home Assistance", "VitalCare Senior Support", "EverSafe In-Home Services",
    "TrueCare Health Solutions", "SereneHome Health Agency", "SilverBridge Home Care",
    "GoldenYears Home Support", "Harmony Senior Assistance", "Guardian Angel Home Care",
    "TranquilLiving Senior Services", "NobleCare Home Health", "EliteCare In-Home Services", "CareLiving Home Health",
    "HomeSafe Services"
]

location_data = {
    "California": [("Los Angeles", 90001), ("San Francisco", 94101), ("San Diego", 92101), ("Sacramento", 95814)],
    "Texas": [("Houston", 77001), ("Austin", 73301), ("Dallas", 75201)],
    "Florida": [("Miami", 33101), ("Orlando", 32801)],
    "New York": [("New York City", 10001), ("Buffalo", 14201), ("Rochester", 14602)],
    "Illinois": [("Chicago", 60601), ("Springfield", 62701),],
    "Arizona": [("Phoenix", 85001)],
    "Ohio": [("Columbus", 43201)],
}


customer_dataset = []
customer_ids = list(range(1001, 1001 + len(customers)))  # Generate unique IDs

for i, customer in enumerate(customers):
    state = random.choice(list(location_data.keys()))
    city, zip_code_prefix = random.choice(location_data[state])
    
    customer_dataset.append({
        "customer_id": f"CUS{str(i+1).zfill(3)}",
        "customer_name": customer,
        "customer_city": city,
        "customer_state": state,
        "customer_zip_code_prefix": zip_code_prefix
    })

df_customer = pd.DataFrame(customer_dataset)
df_customer


# In[84]:


def get_thanksgiving_date(year):
    """Calculate Thanksgiving date (4th Thursday of November)."""
    november_first = datetime(year, 11, 1)
    weekday = november_first.weekday()
    days_to_thursday = (3 - weekday + 7) % 7  # Days until first Thursday
    return november_first + timedelta(days=days_to_thursday + 21)  # Add 3 weeks

# Define the holiday periods
thanksgiving_date = get_thanksgiving_date(2024)
christmas_date = datetime(2024, 12, 25)

thanksgiving_week_start = (thanksgiving_date - timedelta(days=7)).date()
thanksgiving_week_end = (thanksgiving_date + timedelta(days=7)).date()
christmas_week_start = (christmas_date - timedelta(days=7)).date()
christmas_week_end = (christmas_date + timedelta(days=7)).date()

# list of customers, sales reps and location

sales_reps = ["John Smith", "Sarah Johnson", "David Brown", "Emily Davis", "James Wilson", 
              "Michael Anderson", "Olivia Clark", "Daniel Taylor", "David Smith", "Ben Lee", "Jessica Davis", 
             "Micheal Johnson", "Dan Miller", "Ashley Taylor", "Paul Lee", "Mary Kim"]

# Random seed for reproducibility
random.seed(42)

orders_data = []

for order_id in range(10001, 20001):  # Create 10000 sales records
    # Randomly select a product, customer and sales rep
    
    product = df_item[df_item['product_id'] == product_id].iloc[0]    
    product_id = random.choice(df_item['product_id'])  # Randomly select product_id from product_pricing
    
    customer = random.choice(df_customer['customer_id'])
    sales_rep = random.choice(sales_reps)
    
    # Generate a random date in 2024
    order_date = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 364))).date()
    
    # Adjust sales volume and discount rates
    if thanksgiving_week_start <= sale_date <= thanksgiving_week_end or christmas_week_start <= sale_date <= christmas_week_end:
        quantity_sold = random.randint(50, 151)  # Higher sales volume
        discount_rate = round(random.uniform(0.15, 0.20),2)  # 15-25% discount
    elif product['category'] == 'Continence Care':  
        quantity_sold = random.randint(10, 51)  # Normal sales volume  
        discount_rate = round(random.uniform(0.20, 0.25),2)  # 20-25% discount  
    else:  
        quantity_sold = random.randint(10, 51)  # Normal sales volume  
        discount_rate = round(random.uniform(0, 0.15),2)  # 0-15% discount  

    listed_price = product['retail_price']
    final_price = listed_price * (1 - discount_rate)  # Apply discount
    total_sale = final_price * quantity_sold
    cost_per_unit = product['cost']
    total_cost = cost_per_unit * quantity_sold
    profit = total_sale - total_cost

    orders_data.append([
        order_id, product_id, order_date, quantity_sold, listed_price, 
        discount_rate, final_price, total_sale, cost_per_unit, 
        total_cost, profit, sales_rep, customer
    ])
    
    df_orders = pd.DataFrame(orders_data, columns=[
    'order_id', 'product_id', 'order_date', 'quantity_sold', 'listed_price', 
    'discount_rate', 'final_price', 'total_sale', 'cost_per_unit', 
    'total_cost', 'profit', 'sales_rep', 'customer_id'
    ])


# In[86]:


df_orders.head()


# In[87]:


df_orders.isnull().any()


# In[88]:


# Define possible order statuses
order_statuses = ["delivered", "cancelled"]  # Other statuses like "shipped", "processing" are removed for now

# Initialize shipment data list
shipment_data = []

for _, row in df_orders.iterrows():
    order_id = row['order_id']
    
    # Order purchase timestamp (same as sale_date but with random time)
    order_purchase_timestamp = datetime.combine(row['order_date'], 
                                                datetime.min.time()) + timedelta(
                                                    hours=random.randint(8, 20), 
                                                    minutes=random.randint(0, 59)
                                                )

    # Assign random order status
    order_status = random.choices(
        order_statuses, 
        weights=[0.9329, 0.0671]  # 93.29% delivered, 6.71% cancelled
    )[0]

    # Estimated delivery date (3 to 10 days from purchase)
    order_estimated_delivery_date = order_purchase_timestamp + timedelta(days=random.randint(3, 10))

    # Delivered timestamp (if not cancelled)
    if order_status == "delivered":
        # Delivered within -3 to +3 days around the estimated date
        order_delivered_timestamp = order_estimated_delivery_date + timedelta(days=random.randint(-3, 3))
        # Calculate delivery delay (make sure it's >= 0)
        delivery_delay_days = max(0, (order_delivered_timestamp - order_estimated_delivery_date).days)
        # Calculate shipping time
        shipping_time_days = (order_delivered_timestamp - order_purchase_timestamp).days
        # Assign return status (90% Not Returned, 10% Returned)
        return_status = random.choices(["Not Returned", "Returned"], weights=[0.90, 0.0965])[0]
    else:
        order_delivered_timestamp = None  # No delivery for cancelled orders
        delivery_delay_days = None
        shipping_time_days = None
        return_status = None  # No return for cancelled orders

    # Assign shipping carrier (mostly In-House, 5% external carriers)
    shipping_carrier = random.choices(["In-House", "FedEx", "UPS", "DHL"], weights=[0.95, 0.02, 0.02, 0.01])[0]

    # Append record
    shipment_data.append([
        order_id, order_status, order_purchase_timestamp, order_delivered_timestamp, 
        order_estimated_delivery_date, delivery_delay_days, shipping_time_days, 
        shipping_carrier, return_status
    ])

# Create Shipment DataFrame
df_shipment = pd.DataFrame(shipment_data, columns=[
    'order_id', 'order_status', 'order_purchase_timestamp', 
    'order_delivered_timestamp', 'order_estimated_delivery_date', 
    'delivery_delay_days', 'shipping_time_days', 'shipping_carrier', 'return_status'
])

# Display first few rows
df_shipment.head()


# In[89]:


import sqlite3
conn = sqlite3.connect(":memory:")


# In[90]:


df_item.to_sql("df_item", conn, index=False, if_exists="replace")
df_orders.to_sql("df_orders", conn, index=False, if_exists="replace")
df_shipment.to_sql("df_shipment", conn, index=False, if_exists="replace")
df_customer.to_sql("df_customer", conn, index=False, if_exists="replace")


# In[91]:


query = """
SELECT
o.order_id,
o.product_id,
o.order_date,
o.quantity_sold,
o.listed_price,
o.discount_rate,
o.final_price,
o.total_sale,
o.cost_per_unit,
o.total_cost,
o.profit,
o.sales_rep,
o.customer_id,


i.product_name, 
i.category, 
i.brand, 
i.unit_of_measure, 
i.cost AS item_cost, 
i.retail_price AS item_retail_price,

s.order_status, 
s.order_purchase_timestamp, 
s.order_delivered_timestamp, 
s.order_estimated_delivery_date, 
s.delivery_delay_days, 
s.shipping_time_days, 
s.shipping_carrier, 
s.return_status,
c.customer_name, 
c.customer_city, 
c.customer_state, 
c.customer_zip_code_prefix

FROM df_orders AS o
JOIN df_item AS i
ON o.product_id = i.product_id
JOIN df_shipment AS s
ON o.order_id = s.order_id
JOIN df_customer AS c
ON o.customer_id = c.customer_id
"""


# In[92]:


integrated_df = pd.read_sql_query(query, conn)

print(integrated_df.head())


# In[93]:


df_item.to_csv('df_item.csv', index=False)
df_orders.to_csv('df_orders.csv', index=False)
df_customer.to_csv('df_customer.csv', index=False)
df_shipment.to_csv('df_shipment.csv', index=False)
integrated_df.to_csv('integrated_df.csv', index=False)


# In[ ]:




