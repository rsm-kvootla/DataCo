#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pandas as pd
import numpy as np


# In[36]:


df = pd.read_csv('datanew2.csv')


# In[37]:


df['late'] = df['days_for_shipping_(real)'] > df['days_for_shipment_(scheduled)']


# In[38]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, roc_auc_score


# Define features and target variable
features = ['type', 'days_for_shipment_(scheduled)', 'shipping_mode', 
            'order_region', 'order_status', 'benefit_per_order', 
            'sales_per_customer', 'customer_city', 'customer_state', 
            'category_name', 'product_price', 'latitude', 'longitude']
target = 'late'

X = df[features]
y = df[target]

# Preprocess the data
categorical_features = ['type', 'shipping_mode', 'order_region', 'order_status', 
                        'customer_city', 'customer_state', 'category_name']
numerical_features = ['days_for_shipment_(scheduled)', 'benefit_per_order', 
                      'sales_per_customer', 'product_price', 'latitude', 'longitude']

# One-hot encode categorical variables and scale numerical variables
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first'), categorical_features),
        ('num', StandardScaler(), numerical_features)
    ]
)
X_processed = preprocessor.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Train Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluate the model
print("Classification Report:\n", classification_report(y_test, y_pred))
print("ROC AUC Score:", roc_auc_score(y_test, y_pred_proba))


# In[39]:


importances = model.feature_importances_
feature_names = preprocessor.get_feature_names_out()
feature_importances = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
print(feature_importances.sort_values(by='Importance', ascending=False))


# In[40]:


threshold = 0.6
y_pred_custom = (y_pred_proba >= threshold).astype(int)
print("Adjusted Classification Report:\n", classification_report(y_test, y_pred_custom))


# In[41]:


print(df['late'].dtype)
import scipy.stats as stats

# Select only the factor variables (categorical variables)
factor_vars = df.select_dtypes(include=['object', 'bool']).columns

# List to store significant variables
significant_vars = []

# Run chi-square test for each factor variable in relation to 'late'
for var in factor_vars:
    contingency_table = pd.crosstab(df[var], df['late'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    print(f"Chi-square test for {var}:")
    print(f"Chi2: {chi2}, p-value: {p}\n")
    if p < 0.05:
        significant_vars.append(var)

print("Significant variables with p-value < 0.05:")
print(significant_vars)


# In[42]:


from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import log_loss

# Define features and target
features = ['type', 'days_for_shipment_(scheduled)', 'shipping_mode', 
            'order_region', 'order_status', 'benefit_per_order', 
            'sales_per_customer', 'category_name', 'product_price', 'latitude', 'longitude']
target = 'late'

X = df[features]
y = df[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocess the data
categorical_features = ['type', 'shipping_mode', 'order_region', 'order_status', 'category_name']
numerical_features = ['days_for_shipment_(scheduled)', 'benefit_per_order', 'sales_per_customer', 'product_price', 'latitude', 'longitude']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first'), categorical_features),
        ('num', StandardScaler(), numerical_features)
    ]
)

# Create a pipeline for logistic regression
logistic_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=500, class_weight='balanced'))  # Add class weights if needed
])

# Train the logistic regression model
logistic_pipeline.fit(X_train, y_train)

# Make predictions
y_pred_proba = logistic_pipeline.predict_proba(X_test)[:, 1]  # Probabilities for the positive class
y_pred = (y_pred_proba >= 0.5).astype(int)  # Use a default threshold of 0.5

# Evaluate the model
print("Classification Report:\n", classification_report(y_test, y_pred))
print("ROC AUC Score:", roc_auc_score(y_test, y_pred_proba))
print("Log-Loss:", log_loss(y_test, y_pred_proba))

# Adjust the threshold for predictions (optional)
threshold = 0.6  # Example: Use 0.6 to minimize false negatives
y_pred_custom = (y_pred_proba >= threshold).astype(int)

print("\nAdjusted Classification Report (Threshold = 0.6):\n", classification_report(y_test, y_pred_custom))


# In[43]:


# Feature Engineering
# 1. Interaction terms: Create interactions between important features
df['shipment_efficiency'] = df['days_for_shipment_(scheduled)'] / (df['benefit_per_order'] + 1)
df['price_per_customer'] = df['product_price'] / (df['sales_per_customer'] + 1)

# 2. Extract categorical feature information (if applicable)
df['is_high_value_order'] = (df['benefit_per_order'] > 50).astype(int)

# 3. Encoding date features (e.g., shipping or order date)
df['order_weekday'] = pd.to_datetime(df['order_date_(dateorders)']).dt.weekday
df['is_weekend'] = df['order_weekday'].isin([5, 6]).astype(int)


# In[44]:


# Correlation matrix
corr_matrix = df.select_dtypes(include=[np.number]).corr()

# Select features with high correlation (absolute correlation > 0.8)
high_corr_features = [column for column in corr_matrix.columns if any(abs(corr_matrix[column]) > 0.8)]
print("Highly correlated features to review for removal:", high_corr_features)


# In[45]:


# Drop redundant or highly correlated features
features_to_drop = [
    'days_for_shipping_(real)', 'latitude', 'longitude', 'order_id', 
    'order_customer_id', 'customer_id', 'customer_zipcode', 
    'department_id', 'order_item_cardprod_id', 'order_item_discount',
    'order_item_discount_rate', 'order_item_id', 'order_item_product_price', 
    'order_item_profit_ratio', 'sales', 'order_item_total', 'order_profit_per_order', 
    'product_card_id', 'product_category_id', 'benefit_per_order', 
    'product_price', 'sales_per_customer'
]
df = df.drop(columns=features_to_drop)

print("Remaining Features:", df.columns)


# In[46]:


# Define updated features
features = [
    'type', 'shipping_mode', 'order_region', 'order_status', 
    'shipment_efficiency', 'price_per_customer', 'is_high_value_order', 
    'order_weekday', 'is_weekend'
]

X = df[features]
y = df[target]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocess categorical and numerical features
categorical_features = ['type', 'shipping_mode', 'order_region', 'order_status']
numerical_features = ['shipment_efficiency', 'price_per_customer', 'is_high_value_order', 'order_weekday', 'is_weekend']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first'), categorical_features),
        ('num', StandardScaler(), numerical_features)
    ]
)

# Train logistic regression with the simplified dataset
logistic_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=500, class_weight='balanced'))
])

logistic_pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred_proba = logistic_pipeline.predict_proba(X_test)[:, 1]
y_pred = (y_pred_proba >= 0.5).astype(int)

print("Simplified Model - Classification Report:\n", classification_report(y_test, y_pred))
print("Simplified Model - ROC AUC Score:", roc_auc_score(y_test, y_pred_proba))


# In[47]:


# Adjust threshold to minimize false negatives (e.g., improve recall for late deliveries)
threshold = 0.4  # Adjust this value as needed
y_pred_custom = (y_pred_proba >= threshold).astype(int)

print("Adjusted Classification Report (Threshold = 0.4):\n", classification_report(y_test, y_pred_custom))


# In[48]:


# Test different thresholds
thresholds = [0.3, 0.35, 0.4, 0.45, 0.5]
for threshold in thresholds:
    y_pred_custom = (y_pred_proba >= threshold).astype(int)
    print(f"Threshold: {threshold}")
    print(classification_report(y_test, y_pred_custom))


# 1.	Threshold: 0.3
# - Recall (True): 99% - Very high recall for predicting late deliveries (True class), meaning almost all late deliveries are captured.
# - Precision (True): 57% - Precision drops significantly, meaning many false positives (on-time predicted as late).
# - Accuracy: 57% - Overall accuracy suffers due to a high number of false positives.
# 2.	Threshold: 0.35
# - Recall (True): 66% - Recall improves compared to the default threshold but drops from 99% at 0.3.
# - Precision (True): 75% - Better balance between precision and recall.
# - Accuracy: 68% - Higher than threshold 0.3 but still slightly lower than 0.4.
# 3.	Threshold: 0.4
# - Recall (True): 58% - Captures fewer late deliveries compared to lower thresholds but has fewer false positives.
# - Precision (True): 84% - Highest precision among the thresholds, with better identification of true late deliveries.
# - Accuracy: 70% - Best overall accuracy.

# Recommendation
# 1.	If Recall is a Priority (e.g., minimizing missed late deliveries):
# Use Threshold 0.35:
# It balances recall (66%) and precision (75%) well.
# Accuracy (68%) is acceptable.
# 2.	If Precision and Accuracy are More Important:
# Use Threshold 0.4:
# Best overall accuracy (70%).
# High precision (84%) ensures that predicted late deliveries are mostly correct.

# In[49]:


# Logistic regression coefficients for feature importance
coefficients = logistic_pipeline.named_steps['classifier'].coef_[0]
cat_feature_names = logistic_pipeline.named_steps['preprocessor'].transformers_[0][1].get_feature_names_out()
num_feature_names = numerical_features
feature_names = np.concatenate([cat_feature_names, num_feature_names])
feature_importance = pd.DataFrame({'Feature': feature_names, 'Coefficient': coefficients})
feature_importance['Abs_Coefficient'] = feature_importance['Coefficient'].abs()
feature_importance = feature_importance.sort_values(by='Abs_Coefficient', ascending=False)

print(feature_importance.head(10))  # Top 10 important features


# In[50]:


for region in df['order_region'].unique():
    subset = X_test[df['order_region'] == region]
    subset_y = y_test[df['order_region'] == region]
    subset_pred = logistic_pipeline.predict(subset)
    print(f"Performance for Region {region}:")
    print(classification_report(subset_y, subset_pred))


# In[51]:


from sklearn.model_selection import cross_val_score

scores = cross_val_score(logistic_pipeline, X, y, cv=5, scoring='roc_auc')
print("Cross-validated ROC AUC scores:", scores)
print("Average ROC AUC:", scores.mean())


# In[52]:


from sklearn.metrics import precision_recall_curve, roc_curve
import matplotlib.pyplot as plt

precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
plt.plot(thresholds, precision[:-1], label='Precision')
plt.plot(thresholds, recall[:-1], label='Recall')
plt.xlabel('Threshold')
plt.ylabel('Score')
plt.legend()
plt.show()


# In[53]:


false_positives = X_test[(y_test == 0) & (y_pred == 1)]
false_negatives = X_test[(y_test == 1) & (y_pred == 0)]
print("False Positives Sample:")
print(false_positives.head())
print("False Negatives Sample:")
print(false_negatives.head())


# In[54]:


from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

importance = permutation_importance(logistic_pipeline, X_test, y_test, n_repeats=10, random_state=42)
sorted_idx = importance.importances_mean.argsort()
plt.barh(range(len(sorted_idx)), importance.importances_mean[sorted_idx], align='center')
plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
plt.xlabel("Feature Importance")
plt.show()


# 1.	Region-Specific Performance:
# - The performance of the model varies across regions. For instance:
# - West of USA shows a good balance between precision and recall for the “True” class.
# - Central America has similar precision, but recall is slightly lower.
# - South America’s recall is lower compared to others.
# - This indicates the model’s predictive power is region-dependent.
# 2.	Cross-Validation Results:
# - Cross-validation shows an average ROC AUC of ~0.74, which confirms the model has a moderate ability to distinguish between late and on-time deliveries across different splits of the data.
# - This is consistent with the testing set’s ROC AUC, validating the model’s robustness.
# 3.	Feature Importance:
# - Features like shipping_mode and order_status have significant influence on the predictions.
# - shipping_mode_Standard Class and shipping_mode_Same Day have negative coefficients, meaning they reduce the likelihood of late delivery.
# 4.	Precision-Recall Tradeoff:
# - By adjusting the threshold (e.g., 0.3, 0.35, 0.4), you can trade between precision and recall based on business needs.
# - For example, a threshold of 0.4 improves recall for late deliveries, ensuring fewer false negatives.

# In[55]:


region_specific_models = {}
for region in df['order_region'].unique():
    subset_X = X[df['order_region'] == region]
    subset_y = y[df['order_region'] == region]
    
    # Preprocess the subset data
    subset_X_processed = preprocessor.transform(subset_X)
    
    model = LogisticRegression(max_iter=500, class_weight='balanced')
    model.fit(subset_X_processed, subset_y)
    region_specific_models[region] = model


# In[56]:


from sklearn.metrics import precision_recall_curve
optimal_threshold = None
max_f1 = 0
precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
for p, r, t in zip(precision, recall, thresholds):
    f1 = 2 * (p * r) / (p + r)
    if f1 > max_f1:
        max_f1 = f1
        optimal_threshold = t
print(f"Optimal Threshold: {optimal_threshold}, Max F1: {max_f1}")


# In[57]:


# Define a new preprocessor for the simplified dataset
simplified_categorical_features = ['shipping_mode', 'type', 'order_status', 'order_region']
simplified_preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first'), simplified_categorical_features)
    ]
)


# In[58]:


# Align indices of features and labels
simplified_X = X.loc[y_train.index, simplified_categorical_features]
simplified_X_processed = simplified_preprocessor.fit_transform(simplified_X)


# In[59]:


# Select the simplified features
simplified_features = ['shipping_mode', 'type', 'order_status', 'order_region']
simplified_X = X[simplified_features]

# Align indices of features and labels
simplified_X = X.loc[y_train.index, simplified_features]

# Transform the simplified dataset
simplified_X_processed = simplified_preprocessor.fit_transform(simplified_X)

# Train the logistic regression model
simplified_model = LogisticRegression(max_iter=500, class_weight='balanced')
simplified_model.fit(simplified_X_processed, y_train)

# Evaluate the simplified model
y_pred_simplified = simplified_model.predict(simplified_X_processed)
print("Simplified Model Performance:")
print(classification_report(y_train, y_pred_simplified))


# In[60]:


from sklearn.metrics import precision_recall_curve, roc_curve

# Calculate precision, recall, and thresholds
precision, recall, thresholds = precision_recall_curve(y_train, simplified_model.predict_proba(simplified_X_processed)[:, 1])

# Find the optimal threshold (maximizing F1-Score)
optimal_threshold = None
max_f1 = 0
for p, r, t in zip(precision, recall, thresholds):
    f1 = 2 * (p * r) / (p + r) if (p + r) > 0 else 0
    if f1 > max_f1:
        max_f1 = f1
        optimal_threshold = t

print(f"Optimal Threshold: {optimal_threshold}, Max F1: {max_f1}")

# Apply the optimal threshold
y_pred_optimized = (simplified_model.predict_proba(simplified_X_processed)[:, 1] >= optimal_threshold).astype(int)

# Evaluate with the optimal threshold
from sklearn.metrics import classification_report
print("Performance with Optimal Threshold:")
print(classification_report(y_train, y_pred_optimized))


# In[82]:


# Ensure 'order_region' is included in the features
if 'order_region' not in simplified_features:
    simplified_features.append('order_region')

# Select the simplified features
simplified_X = X[simplified_features]

# Ensure indices of X and y are aligned
simplified_X = simplified_X.loc[y_train.index]

# Evaluate the model for each region
for region in simplified_X['order_region'].unique():
    # Subset the data for the region
    region_X = simplified_X[simplified_X['order_region'] == region]
    region_y = y_train.loc[region_X.index]  # Align y labels with the subset X indices
    
    # Transform the subset data
    region_X_processed = simplified_preprocessor.transform(region_X)
    
    # Predict using the simplified model
    region_y_pred = simplified_model.predict(region_X_processed)
    
    # Print performance metrics for the region
    print(f"Performance for Region {region}:")
    print(classification_report(region_y, region_y_pred))
    
    # Save the performance metrics for each region as a DataFrame
    performance_metrics = []

    for region in simplified_X['order_region'].unique():
        # Subset the data for the region
        region_X = simplified_X[simplified_X['order_region'] == region]
        region_y = y_train.loc[region_X.index]  # Align y labels with the subset X indices
        
        # Transform the subset data
        region_X_processed = simplified_preprocessor.transform(region_X)
        
        # Predict using the simplified model
        region_y_pred = simplified_model.predict(region_X_processed)
        
        # Calculate performance metrics
        report = classification_report(region_y, region_y_pred, output_dict=True)
        performance_metrics.append({
            'Region': region,
            'Precision_True': report['True']['precision'],
            'Recall_True': report['True']['recall'],
            'F1-Score_True': report['True']['f1-score'],
            'Precision_False': report['False']['precision'],
            'Recall_False': report['False']['recall'],
            'F1-Score_False': report['False']['f1-score']
        })

    # Convert the list of dictionaries to a DataFrame
    performance_metrics_df = pd.DataFrame(performance_metrics)
    print(performance_metrics_df)


# In[62]:


# Train a baseline model (e.g., Decision Tree Classifier)
from sklearn.tree import DecisionTreeClassifier

baseline_model = DecisionTreeClassifier(max_depth=5, random_state=42, class_weight='balanced')
baseline_model.fit(simplified_X_processed, y_train)

# Evaluate the baseline model
baseline_y_pred = baseline_model.predict(simplified_X_processed)
print("Baseline Model Performance:")
print(classification_report(y_train, baseline_y_pred))


# In[63]:


# Retrieve feature names from the preprocessor
from sklearn.compose import ColumnTransformer

# Ensure you get the names of the one-hot encoded columns
encoded_feature_names = simplified_preprocessor.named_transformers_['cat'].get_feature_names_out(simplified_categorical_features)

# Combine all feature names (only categorical here as no numerical in simplified features)
final_feature_names = encoded_feature_names

# Retrieve coefficients from the logistic regression model
coefficients = simplified_model.coef_[0]

# Create a DataFrame for feature importance
feature_importance = pd.DataFrame({
    'Feature': final_feature_names,
    'Coefficient': coefficients
})

# Calculate absolute coefficients for ranking
feature_importance['Abs_Coefficient'] = feature_importance['Coefficient'].abs()

# Sort by absolute coefficient values
feature_importance = feature_importance.sort_values(by='Abs_Coefficient', ascending=False)

# Display the top 10 important features
print("Top 10 Important Features:")
print(feature_importance.head(10))


# 
# 1.	Optimal Threshold and Region-Wise Evaluation:
# - The optimal threshold calculated for the logistic regression model maximizes the F1-score. Using this threshold can help balance precision and recall for the “late delivery” class.
# - The region-wise performance shows variations, indicating that “late delivery” behavior might differ based on geographic regions. These results suggest a possible need for region-specific models or further regional data preprocessing.
# 2.	Baseline Decision Tree Performance:
# - The baseline model (Decision Tree Classifier) provides similar precision and recall values compared to logistic regression but is less interpretable. Its simplicity might be useful if interpretability is not a concern.
# - The baseline model is good for confirming if the logistic regression model’s performance is meaningfully better.\
# 3.	Feature Importance:
# - Logistic regression coefficients highlight key drivers of late delivery. For instance, features like shipping_mode_Standard Class and shipping_mode_Same Day have large negative impacts (significant predictors).
# - These insights could be used for actionable recommendations to improve the business process.

# In[64]:


from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, precision_recall_curve
import joblib  # Correctly importing joblib
import pandas as pd

# Define the simplified features and categorical preprocessing
simplified_features = ['shipping_mode', 'type', 'order_status', 'order_region']
simplified_categorical_features = simplified_features

# Create a preprocessing pipeline for simplified features
simplified_preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first'), simplified_categorical_features)
    ]
)

# Train the final logistic regression model
final_model_pipeline = Pipeline(steps=[
    ('preprocessor', simplified_preprocessor),
    ('classifier', LogisticRegression(max_iter=500, class_weight='balanced', random_state=42))
])

final_model_pipeline.fit(X[simplified_features], y)

# Calculate the optimal threshold based on F1-score
precision, recall, thresholds = precision_recall_curve(y, final_model_pipeline.predict_proba(X[simplified_features])[:, 1])
optimal_threshold = None
max_f1 = 0
for p, r, t in zip(precision, recall, thresholds):
    f1 = 2 * (p * r) / (p + r) if (p + r) > 0 else 0
    if f1 > max_f1:
        max_f1 = f1
        optimal_threshold = t

print(f"Optimal Threshold: {optimal_threshold}, Max F1: {max_f1}")

# Save the final model pipeline and optimal threshold
joblib.dump(final_model_pipeline, 'final_logistic_model.pkl')
joblib.dump(optimal_threshold, 'optimal_threshold.pkl')

# Evaluate the final model with optimal threshold
y_pred_final = (final_model_pipeline.predict_proba(X[simplified_features])[:, 1] >= optimal_threshold).astype(int)
print("Final Model Performance with Optimal Threshold:")
print(classification_report(y, y_pred_final))


# In[65]:


import joblib
joblib.dump(final_model_pipeline, "final_model_pipeline.pkl")


# Nitya's part

# In[76]:


print(region_specific_models)


# In[85]:


import matplotlib.pyplot as plt

# Plot Precision, Recall, and F1-Score for each region
fig, ax = plt.subplots(3, 1, figsize=(10, 15))

# Precision
ax[0].plot(performance_metrics_df['Region'], performance_metrics_df['Precision_True'], label='Precision (True)', marker='o')
ax[0].plot(performance_metrics_df['Region'], performance_metrics_df['Precision_False'], label='Precision (False)', marker='o')
ax[0].set_title('Precision by Region')
ax[0].set_ylabel('Precision')
ax[0].legend()

# Recall
ax[1].plot(performance_metrics_df['Region'], performance_metrics_df['Recall_True'], label='Recall (True)', marker='o')
ax[1].plot(performance_metrics_df['Region'], performance_metrics_df['Recall_False'], label='Recall (False)', marker='o')
ax[1].set_title('Recall by Region')
ax[1].set_ylabel('Recall')
ax[1].legend()

# F1-Score
ax[2].plot(performance_metrics_df['Region'], performance_metrics_df['F1-Score_True'], label='F1-Score (True)', marker='o')
ax[2].plot(performance_metrics_df['Region'], performance_metrics_df['F1-Score_False'], label='F1-Score (False)', marker='o')
ax[2].set_title('F1-Score by Region')
ax[2].set_ylabel('F1-Score')
ax[2].legend()

plt.xlabel('Region')
plt.tight_layout()
plt.show()


# In[86]:


import joblib

# Load the pipeline
final_model_pipeline = joblib.load("final_model_pipeline.pkl")

# Load the optimal threshold (if saved separately)
optimal_threshold = joblib.load("optimal_threshold.pkl")


# In[87]:


#pip install streamlit


# In[88]:


import streamlit as st
import numpy as np

# Load the model pipeline and threshold
final_model_pipeline = joblib.load("final_model_pipeline.pkl")
optimal_threshold = joblib.load("optimal_threshold.pkl")

# Define the app
st.title("Late Delivery Risk Prediction")

# User input fields for each feature
st.header("Enter Delivery Details")
shipping_mode = st.selectbox("Shipping Mode", ["First Class", "Same Day", "Second Class", "Standard Class"])
order_type = st.selectbox("Order Type", ["PAYMENT", "TRANSFER", "DEBIT","CASH"])
order_status = st.selectbox("Order Status", ["PENDING_PAYMENT", "PENDING", "PROCESSING", "ON_HOLD", "COMPLETE", "CLOSED", "SUSPECTED_FRAUD", "CANCELED", "PAYMENT_REVIEW"])
order_region = st.selectbox("Order Region", ["West of USA ", "Central America", "South of USA", "East of USA", "South America"])

# Correct the order_region value if necessary
if order_region == "South of USA":
    order_region = "South of  USA "
    
# Convert inputs into a single-row dataframe
input_data = {
    "shipping_mode": [shipping_mode],
    "type": [order_type],
    "order_status": [order_status],
    "order_region": [order_region],
}

# Predict late delivery
if st.button("Predict"):
    # Convert user input to the format required by the model pipeline
    input_df = pd.DataFrame(input_data)
    probabilities = final_model_pipeline.predict_proba(input_df)[:, 1]  # Probability for the "late" class

    # Compare probability with optimal threshold
    is_late = probabilities[0] >= optimal_threshold
    risk_score = probabilities[0] * 100

    # Display result
    if is_late:
        st.error(f"High Risk of Late Delivery! (Risk Score: {risk_score:.2f}%)")
    else:
        st.success(f"Low Risk of Late Delivery (Risk Score: {risk_score:.2f}%)")

