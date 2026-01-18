import pandas as pd
import os

def load_and_merge_data(data_path='data/'):
    """
    Simulates fetching data from a warehouse and performing a 
    relational join to create a training-ready dataframe.
    """
    print("--- Starting Data Ingestion Pipeline ---")
    
    # Load raw extracts
    try:
        df_customers = pd.read_csv(os.path.join(data_path, 'customers.csv'))
        df_usage = pd.read_csv(os.path.join(data_path, 'usage_logs.csv'))
        df_billing = pd.read_csv(os.path.join(data_path, 'billing.csv'))
    except FileNotFoundError as e:
        print(f"Error: Run src/data_gen.py first to create the data. {e}")
        return None

    # Step 1: Aggregate usage logs (Convert multiple rows per user into one summary row)
    # This shows you understand 'Granularity'
    usage_summary = df_usage.groupby('customer_id').agg({
        'data_usage_gb': ['mean', 'std', 'max'],
        'support_tickets': 'sum',
        'dropped_sessions': 'sum'
    })
    
    # Flatten multi-index columns from the aggregation
    usage_summary.columns = ['_'.join(col).strip() for col in usage_summary.columns.values]
    usage_summary.reset_index(inplace=True)

    # Step 2: Perform the Master Join
    # Left join ensures we keep all customers even if usage/billing is missing
    master_df = pd.merge(df_customers, usage_summary, on='customer_id', how='left')
    master_df = pd.merge(master_df, df_billing, on='customer_id', how='left')

    print(f"Ingestion Complete. Master shape: {master_df.shape}")
    return master_df

if __name__ == "__main__":
    df = load_and_merge_data()
    # Save the 'Intermediate' data for the next step in the pipeline
    if df is not None:
        df.to_csv('data/master_ingested.csv', index=False)
        print("Master file saved to data/master_ingested.csv")