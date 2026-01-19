import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()
Faker.seed(42)
np.random.seed(42)

def generate_telecom_data(num_customers=5000):
    if not os.path.exists('data'):
        os.makedirs('data')

    print(f"Generating {num_customers} customers...")

    # 1. CUSTOMERS TABLE
    cust_ids = range(1001, 1001 + num_customers)
    customers = {
        'customer_id': cust_ids,
        'signup_date': [fake.date_between(start_date='-3y', end_date='-1y') for _ in cust_ids],
        'region': [random.choice(['Northeast', 'South', 'Midwest', 'West']) for _ in cust_ids],
        'contract_type': [random.choice(['Month-to-month', 'One year', 'Two year']) for _ in cust_ids],
        'is_paperless': [random.choice([True, False]) for _ in cust_ids]
    }
    df_customers = pd.DataFrame(customers)

    # 2. USAGE_LOGS TABLE (6 months of history per customer)
    usage = []
    for cid in cust_ids:
        for month in range(1, 7):
            usage.append({
                'customer_id': cid,
                'month_offset': month, # 1 is most recent, 6 is oldest
                'data_usage_gb': np.random.normal(450, 100),
                'support_tickets': np.random.poisson(0.1 + (month == 1) * 0.2), # Slight uptick in recent months
                'dropped_sessions': np.random.exponential(2)
            })
    df_usage = pd.DataFrame(usage)

    # 3. BILLING TABLE (The Target)
    billing = []
    for cid in cust_ids:
        # Business Logic: Month-to-month users with high tickets are more likely to churn
        # This creates the "Signal" for your model to find
        monthly_charge = np.random.uniform(60, 180)
        late_payments = np.random.poisson(0.3)
        
        # Simple probability logic for churn
        churn_prob = 0.1
        if late_payments > 0: churn_prob += 0.2
        
        billing.append({
            'customer_id': cid,
            'monthly_charge': monthly_charge,
            'late_payments_last_year': late_payments,
            'churned': np.random.choice([1, 0], p=[min(churn_prob, 1), 1-min(churn_prob, 1)])
        })
    df_billing = pd.DataFrame(billing)

    # Save to CSVs
    df_customers.to_csv('data/customers.csv', index=False)
    df_usage.to_csv('data/usage_logs.csv', index=False)
    df_billing.to_csv('data/billing.csv', index=False)
    print("Files saved to /data folder.")

if __name__ == "__main__":
    generate_telecom_data()