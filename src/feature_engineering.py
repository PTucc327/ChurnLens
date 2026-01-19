import pandas as pd
import numpy as np
from datetime import datetime

def perform_feature_engineering(input_path = 'data/master_ingested.csv'):
    print("--- Starting Feature Engineering Pipeline ---")
    df = pd.read_csv(input_path)

    # 1. Feature: Promo Expiry Proximity
    # How many days until their promotional discount expires?(Negative means it already ended)
    df['promo_expiry_date'] = pd.to_datetime(df['promo_expiry_date'])
    today = datetime.now()
    df['days_until_promo_expiry'] = (df['promo_expiry_date']-today).dt.days

    # 2. Feature: Usage Velocity
    # We compare recent usage (month 1-2) vs older usage(months 5-6)
    # df_usage from earlier had month_offset (1=recent, 6=oldest)
    df['usage_velocity'] = df['data_usage_gb_mean']/(df['data_usage_gb_mean']+1)


    # 3. Feature: Support Interaction Intesity
    # Tickets per month of tenure
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    df['tenure_days'] = (today - df['signup_date']).dt.days
    df['ticket_intensity'] = df['num_support_tickets']/(df['tenure_days']/30)

    # 4. Encoding Categorical Variables
    # Use one-hot encoding for categorical features
    df = pd.get_dummies(df, columns = ['region','contract_type'], drop_first=True)

    # Clean up NaN values that may have been created
    df.fillna(0, inplace= True)
    print("--- Feature Engineering Pipeline Complete ---")
    print(f'New shape of data: {df.shape}')
    return df


if __name__ == "__main__":
    featured_df = perform_feature_engineering()
    featured_df.to_csv('data/featured_data.csv', index=False)
    print("Featured data saved to 'data/featured_data.csv'")