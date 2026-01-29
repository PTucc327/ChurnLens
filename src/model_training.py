import pandas as pd
import xgboost as xgb
import shap
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from imblearn.over_sampling import SMOTE

def train_churn_model(data_path = 'data/featured_data.csv'):
    print("--- Starting Model Training Pipeline ---")
    df = pd.read_csv(data_path)


    # Define Feature Columns and Target Variable
    X = df.drop(columns=['customer_id', 'signup_date','churned' ])
    y = df['churned']


    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    # Apply Smote to handle class imbalance
    smote = SMOTE(random_state=42)
    X_train, y_train = smote.fit_resample(X_train, y_train)
    

    # Model Initialization and Training
    model = xgb.XGBClassifier(
                              n_estimators=100,
                              learning_rate=0.1,
                              max_depth=5,
                              random_state=42,
                            #   scale_pos_weight= (len(y_train)-sum(y_train)) /sum(y_train)
                              )  # Handle class imbalance
    # Fit model
    model.fit(X_train, y_train)
   
   # Evaluate Model
    y_pred = model.predict(X_test)
    print('Model Performance on Test Set:')
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, model.predict_proba(X_test)[:,1]):.4f}")


    y_probs = model.predict_proba(X_test)[:, 1]
    y_pred_new = (y_probs >= 0.2).astype(int)

    print("--- Performance with 0.2 Threshold ---")
    print(classification_report(y_test, y_pred_new))


    #SHAP Explainability
    explainer = shap.Explainer(model)
    shap_values = explainer(X_test)
    shap.summary_plot(shap_values, X_test, show=False)
    plt.savefig('data/shap_summary_plot.png')

    return model

if __name__ == "__main__":
    trained_model = train_churn_model()
    print("Model training complete. SHAP summary plot saved to 'data/shap_summary_plot.png'")