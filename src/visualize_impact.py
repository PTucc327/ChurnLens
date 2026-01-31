import matplotlib.pyplot as plt
import numpy as np
import os
def generate_roi_dashboard():

    if not os.path.exists('results'):
        os.makedirs('results')
        print("Created 'results' directory.")

    # Model Results (from your 0.2 threshold test)
    total_customers = 1000
    churners_in_data = 163
    caught_churners = 108  # 66% Recall
    false_positives = 427  # Customers incorrectly flagged

    # Financial Assumptions (Industry standard for ISPs like Charter)
    customer_ltv = 1500  # Lifetime Value of a subscriber
    retention_offer_cost = 50 
    save_rate = 0.30  # 30% of people stay if given an offer

    # Calculations
    revenue_protected = caught_churners * save_rate * customer_ltv
    total_offer_cost = (caught_churners + false_positives) * retention_offer_cost
    net_profit = revenue_protected - total_offer_cost

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    metrics = ['Revenue Protected', 'Cost of Offers', 'Net Project Value']
    values = [revenue_protected, total_offer_cost, net_profit]
    colors = ['#2ecc71', '#e74c3c', '#3498db']

    bars = ax.bar(metrics, values, color=colors)
    ax.set_title('ChurnLens: Business Impact Analysis (Per 1,000 Customers)', fontsize=14)
    ax.set_ylabel('Value in USD ($)')
    
    # Add labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'${height:,.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig('results/business_impact_dashboard.png')
    print(f"Dashboard generated! Net Project Value: ${net_profit:,.0f}")

if __name__ == "__main__":
    generate_roi_dashboard()