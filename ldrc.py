#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pandas as pd
import numpy as np


# In[36]:


df = pd.read_csv('datanew2.csv')


# In[37]:


df['late'] = df['days_for_shipping_(real)'] > df['days_for_shipment_(scheduled)']


import joblib

# Load the pipeline
final_model_pipeline = joblib.load("final_model_pipeline.pkl")

# Load the optimal threshold (if saved separately)
optimal_threshold = joblib.load("optimal_threshold.pkl")


# In[87]:


#pip install streamlit


# In[88]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import seaborn as sns
from itertools import product

# Load the model pipeline and threshold
final_model_pipeline = joblib.load("final_model_pipeline.pkl")
optimal_threshold = joblib.load("optimal_threshold.pkl")

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product
import joblib

# Load the model pipeline and threshold
final_model_pipeline = joblib.load("final_model_pipeline.pkl")
optimal_threshold = joblib.load("optimal_threshold.pkl")


# Define the app
st.title("Late Delivery Risk Prediction")

#Late Risk Delivery Trends monitoring chart
st.header("Identifying deliveries with high risk of being late")
# Variable values
shipping_modes = ["First Class", "Same Day", "Second Class", "Standard Class"]
payment_types = ["PAYMENT", "TRANSFER", "DEBIT", "CASH"]
order_statuses = ["PENDING_PAYMENT", "PENDING", "PROCESSING", "ON_HOLD", "COMPLETE", "CLOSED", "SUSPECTED_FRAUD", "CANCELED", "PAYMENT_REVIEW"]
order_regions = ["West of USA ", "Central America", "South of  USA ", "East of USA", "South America"]

# Generate combinations
combinations = list(product(shipping_modes, payment_types, order_statuses, order_regions))
# Create a DataFrame for combinations
combination_df = pd.DataFrame(combinations, columns=["shipping_mode", "type", "order_status", "order_region"])
# Predict late delivery risk for each combination
predictions = final_model_pipeline.predict_proba(combination_df)[:, 1]
combination_df["risk_score_late_delivery"] = predictions

# Add a risk category based on the threshold
combination_df["risk_category"] = np.where(combination_df["risk_score_late_delivery"] >= optimal_threshold, "High Risk", "Low Risk")

# Visualization: Bubble Plot of Late Delivery Risk
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta


# Streamlit dropdown for order_region
selected_region = st.selectbox(
    "Select an Order Region:",
    options=["All"] + combination_df["order_region"].unique().tolist()
)

# Filter data based on selected region
if selected_region != "All":
    filtered_df = combination_df[combination_df["order_region"] == selected_region]
else:
    filtered_df = combination_df

# Create a pivot table for the heatmap
heatmap_data = filtered_df.pivot_table(
    index="shipping_mode",
    columns="type",
    values="risk_score_late_delivery",
    aggfunc="mean"  # Aggregate mean risk score for combinations
).fillna(0)  # Replace NaN with 0

# Create a heatmap
fig = px.imshow(
    heatmap_data,
    labels=dict(x="Payment Type", y="Shipping Mode", color="Risk Score"),
    color_continuous_scale="Reds",  # Choose a color scale
    title=f"Heatmap: Risk Score by Shipping Mode and Payment Type (Region: {selected_region})"
)

# Display the heatmap
st.plotly_chart(fig)


# Display the top risky combinations
st.write("Top 10 Risky Combinations")
risky_combinations = combination_df.sort_values("risk_score_late_delivery", ascending=False).head(10)
st.dataframe(risky_combinations)

# After displaying the heatmap
st.subheader(f"Insights and Recommendations for Region: {selected_region}")

# Generate insights based on the heatmap
high_risk_modes = heatmap_data.idxmax(axis=0).to_dict()
high_risk_payment_types = heatmap_data.idxmax(axis=1).to_dict()

st.write("### Recommendations:")
for payment_type, shipping_mode in high_risk_modes.items():
    if payment_type in heatmap_data.columns:
        try:
            low_risk_shipping_mode = heatmap_data[payment_type].idxmin()
            st.write(f"- **Recommendation for Payment Type: {payment_type}:** Switch to '{low_risk_shipping_mode}' shipping mode for reduced risks.")
        except Exception as e:
            st.write(f"- Unable to determine a lower-risk shipping mode for Payment Type: {payment_type}.")
for shipping_mode, payment_type in high_risk_payment_types.items():
    if shipping_mode in heatmap_data.index:
        try:
            low_risk_payment_type = heatmap_data.loc[shipping_mode].idxmin()
            st.write(f"- **Recommendation for Shipping Mode: {shipping_mode}:** Switch to '{low_risk_payment_type}' payment type for reduced risks.")
        except Exception as e:
            st.write(f"- Unable to determine a lower-risk payment type for Shipping Mode: {shipping_mode}.")

st.write("### Potential Reasons for High Risk:")
st.write("- Higher risks may be due to longer transit times for specific shipping modes.")
st.write("- Payment delays or processing times associated with certain payment methods.")
st.write("- Geographical challenges in certain regions.")


# Map regions to countries
region_to_countries = {
    "West of USA ": ["USA"],
    "Central America": ["Mexico", "Guatemala"],
    "South of  USA ": ["Mexico", "Brazil"],
    "East of USA": ["USA"],
    "South America": ["Brazil", "Argentina"]
}


# Map regions to cities
region_to_cities = {
    "West of USA ": ["Los Angeles", "San Francisco", "Seattle", "Anaheim", "Salt Lake City", "Hesperia", "Murray", "Springfield", "Pasadena"],
    "Central America": ["Mexico City", "Guatemala City","Quetzaltenango", "Escuintla", "Guadalajara"],
    "South of  USA ": ["Houston", "Miami", "Tallahasee", "Columbus", "Florence", "Monroe", "Athens", "Memphis", "West Palm Beach"],
    "East of USA": ["Akron", "Clinton", "Philadelphia", "Auburn", "Columbia", "Buffalo", "Lewiston", "Reading", "Laurel", "Hamilton", "Warwick", "New York City", "Boston", "Washington"],
    "South America": ["São Paulo", "Buenos Aires", "Rio de Janeiro","Brasilia"]
}

# Simulate 100 orders
np.random.seed(42)
regions = np.random.choice(list(region_to_countries.keys()), size=100)
countries = [np.random.choice(region_to_countries[region]) for region in regions]
cities = [np.random.choice(region_to_cities[region]) for region in regions]
order_statuses = ["PENDING_PAYMENT", "PENDING", "PROCESSING", "ON_HOLD", "COMPLETE", "CLOSED", "SUSPECTED_FRAUD", "CANCELED", "PAYMENT_REVIEW"]
shipping_modes = ["First Class", "Same Day", "Second Class", "Standard Class"]
payment_types = ["PAYMENT", "TRANSFER", "DEBIT", "CASH"]
products = [f"Product {i}" for i in range(1, 21)]

simulated_data = pd.DataFrame({
    "order_id": [f"ORD-{i:03d}" for i in range(1, 101)],
    "order_region": regions,
    "order_country": countries,
    "order_city": cities,
    "order_status": np.random.choice(order_statuses, 100),
    "shipping_mode": np.random.choice(shipping_modes, 100),
    "type": np.random.choice(payment_types, 100),
    "product_name": np.random.choice(products, 100),
    "order_date_(dateorders)": [datetime(2023, 1, 1) + timedelta(days=np.random.randint(1, 365)) for _ in range(100)]
})


# Predict late delivery risk based on shipping mode
simulated_data["late_delivery_risk"] = final_model_pipeline.predict_proba(simulated_data[["shipping_mode","order_status","type","order_region"]])[:, 1]
simulated_data["risk_category"] = np.where(simulated_data["late_delivery_risk"] >= optimal_threshold, "High Risk", "Low Risk")

# User selection
st.header("Risk of Late Delivery for current orders")

# Region selection
selected_region = st.selectbox("Select Order Region", ["All"] + list(region_to_countries.keys()))

if selected_region != "All":
    # Filter countries based on selected region
    region_countries = region_to_countries[selected_region]
    filtered_data = simulated_data[simulated_data["order_region"] == selected_region]
else:
    # When "All" is selected for the region, do not filter the DataFrame and show "All" in the country dropdown
    region_countries = ["All"]
    filtered_data = simulated_data

# Country selection
selected_country = st.selectbox("Select Order Country", region_countries)

if selected_country != "All":
    # Further filter data if a specific country is selected
    filtered_data = filtered_data[filtered_data["order_country"] == selected_country]

# Display the filtered data
st.write("Filtered Order Data")
st.dataframe(filtered_data)

# Pie chart for risk category division
st.subheader("Order Division by Risk Category")
st.write(f"**Optimal Threshold for High Risk**: {optimal_threshold:.2f}")

risk_counts = filtered_data["risk_category"].value_counts()
fig1, ax1 = plt.subplots(figsize=(2, 2))
ax1.pie(
    risk_counts, labels=risk_counts.index, autopct="%1.1f%%", colors=["red", "green"], textprops={'fontsize': 5}
)
ax1.set_title("Distribution of order based on risk of delivery compared to optimal threshold ")
st.pyplot(fig1)

# Display high-risk orders
st.subheader("List of High-Risk Orders")
high_risk_orders = filtered_data[filtered_data["risk_category"] == "High Risk"]
st.dataframe(high_risk_orders)


# Order selection
selected_order_id = st.selectbox("Select Order ID", filtered_data["order_id"])
selected_order = filtered_data[filtered_data["order_id"] == selected_order_id]

# Display selected order details
if not selected_order.empty:
    st.write("Selected Order Details:")
    st.dataframe(selected_order)

    risk_score = selected_order["late_delivery_risk"].values[0]
    risk_category = "High Risk" if risk_score >= optimal_threshold else "Low Risk"
    st.write(f"**Late Delivery Risk Prediction:** {risk_category} ({risk_score:.2f})")
else:
    st.warning("No order selected.")

# Define plot function
def plot_selected_order_trends(data, selected_order, fig):
    """Plots trends based on the selected order attributes."""
    # Extract the relevant attributes
    order_status = selected_order["order_status"].iloc[0]
    shipping_mode = selected_order["shipping_mode"].iloc[0]
    payment_type = selected_order["type"].iloc[0]

    # Ensure datetime and quarters
    data["Quarter"] = pd.to_datetime(data["order_date_(dateorders)"]).dt.to_period("Q")
    all_quarters = pd.period_range("2015Q1", "2017Q4", freq="Q")

    # Subplot 1: Stacked bar chart for late vs. on-time deliveries (order status)
    ax1 = fig.add_subplot(3, 2, 1)
    status_data = data[data["order_status"] == order_status]
    status_quarterly = status_data.groupby(["Quarter", "late"]).size().unstack(fill_value=0)
    status_quarterly = status_quarterly.reindex(all_quarters, fill_value=0)
    percentage_status = status_quarterly.div(status_quarterly.sum(axis=1), axis=0) * 100
    percentage_status.plot(kind="bar", stacked=True, color=["red", "green"], ax=ax1)
    ax1.set_title(f"% Late vs. On-Time Deliveries (Order Status: {order_status})")
    ax1.set_xlabel("Quarter")
    ax1.set_ylabel("Percentage")

    # Subplot 2: Average number of days late (order status)
    ax2 = fig.add_subplot(3, 2, 2)
    avg_days_status = status_data[status_data["late"] == True].groupby("Quarter")["late?"].mean()
    avg_days_status = avg_days_status.reindex(all_quarters, fill_value=0)
    avg_days_status.plot(kind="bar", color="red", ax=ax2)
    ax2.set_title(f"Average Days Late (Order Status: {order_status})")
    ax2.set_xlabel("Quarter")
    ax2.set_ylabel("Average Days Late")

    # Subplot 3: Stacked bar chart for late vs. on-time deliveries (shipping mode)
    ax3 = fig.add_subplot(3, 2, 3)
    shipping_data = data[data["shipping_mode"] == shipping_mode]
    shipping_quarterly = shipping_data.groupby(["Quarter", "late"]).size().unstack(fill_value=0)
    shipping_quarterly = shipping_quarterly.reindex(all_quarters, fill_value=0)
    percentage_shipping = shipping_quarterly.div(shipping_quarterly.sum(axis=1), axis=0) * 100
    percentage_shipping.plot(kind="bar", stacked=True, color=["red", "green"], ax=ax3)
    ax3.set_title(f"% Late vs. On-Time Deliveries (Shipping Mode: {shipping_mode})")
    ax3.set_xlabel("Quarter")
    ax3.set_ylabel("Percentage")

    # Subplot 4: Average number of days late (shipping mode)
    ax4 = fig.add_subplot(3, 2, 4)
    avg_days_shipping = shipping_data[shipping_data["late"] == True].groupby("Quarter")["late?"].mean()
    avg_days_shipping = avg_days_shipping.reindex(all_quarters, fill_value=0)
    avg_days_shipping.plot(kind="bar", color="red", ax=ax4)
    ax4.set_title(f"Average Days Late (Shipping Mode: {shipping_mode})")
    ax4.set_xlabel("Quarter")
    ax4.set_ylabel("Average Days Late")

    # Subplot 5: Stacked bar chart for late vs. on-time deliveries (payment type)
    ax5 = fig.add_subplot(3, 2, 5)
    payment_data = data[data["type"] == payment_type]
    payment_quarterly = payment_data.groupby(["Quarter", "late"]).size().unstack(fill_value=0)
    payment_quarterly = payment_quarterly.reindex(all_quarters, fill_value=0)
    percentage_payment = payment_quarterly.div(payment_quarterly.sum(axis=1), axis=0) * 100
    percentage_payment.plot(kind="bar", stacked=True, color=["red", "green"], ax=ax5)
    ax5.set_title(f"% Late vs. On-Time Deliveries (Payment Type: {payment_type})")
    ax5.set_xlabel("Quarter")
    ax5.set_ylabel("Percentage")

    # Subplot 6: Average number of days late (payment type)
    ax6 = fig.add_subplot(3, 2, 6)
    avg_days_payment = payment_data[payment_data["late"] == True].groupby("Quarter")["late?"].mean()
    avg_days_payment = avg_days_payment.reindex(all_quarters, fill_value=0)
    avg_days_payment.plot(kind="bar", color="red", ax=ax6)
    ax6.set_title(f"Average Days Late (Payment Type: {payment_type})")
    ax6.set_xlabel("Quarter")
    ax6.set_ylabel("Average Days Late")

# Create the figure and plot
fig = plt.figure(figsize=(15, 15))
plot_selected_order_trends(df, selected_order, fig)
plt.subplots_adjust(hspace=0.4)  # Increase the vertical spacing between plots
st.pyplot(fig)
# For the selected order
if not selected_order.empty:
    st.subheader("Recommendations for Selected Order")
    # Extract selected order details
    selected_shipping_mode = selected_order["shipping_mode"].iloc[0]
    selected_payment_type = selected_order["type"].iloc[0]
    selected_risk_score = selected_order["late_delivery_risk"].iloc[0]

    # Provide recommendations
    if selected_risk_score >= optimal_threshold:
        st.write(f"The selected order has a **High Risk** of late delivery (Risk Score: {selected_risk_score:.2f}).")
        
        # Check and recommend lower-risk shipping mode
        if selected_payment_type in heatmap_data.columns:
            recommended_shipping = heatmap_data[selected_payment_type].idxmin()
            st.write(f"- **Switch to '{recommended_shipping}' shipping mode to reduce risk'.**")
        
        # Check and recommend lower-risk payment type
        if selected_shipping_mode in heatmap_data.index:
            recommended_payment = heatmap_data.loc[selected_shipping_mode].idxmin()
            st.write(f"- **Switch to '{recommended_payment}' payment type to reduce risk'.**")
    else:
        st.write("The selected order has a **Low Risk** of late delivery. No changes recommended.")

# Display warnings or further recommendations
st.write("**General Advice:**")
st.write("- Streamline payment processing systems to minimize delays.")
st.write("- Use real-time tracking for shipments in high-risk regions.")
st.write("- Offer expedited shipping options for time-sensitive deliveries.")
st.write("- Alert customers about potential delays due to external factors.")

#Simulating affect of recommendations

# Filter late orders
late_orders = simulated_data[simulated_data["risk_category"] == "High Risk"]

# Initialize lists to store results
recommended_changes = []
new_risk_scores_shipping = []
new_risk_scores_payment = []
new_risk_scores_both = []

# Iterate through late orders
for _, order in late_orders.iterrows():
    current_shipping_mode = order["shipping_mode"]
    current_payment_type = order["type"]

    # Recommend a new shipping mode and payment type
    recommended_shipping = heatmap_data.loc[:, current_payment_type].idxmin()
    recommended_payment = heatmap_data.loc[current_shipping_mode].idxmin()

    # Predict risk scores with updates
    updated_shipping_risk = heatmap_data.loc[recommended_shipping, current_payment_type]
    updated_payment_risk = heatmap_data.loc[current_shipping_mode, recommended_payment]
    updated_both_risk = heatmap_data.loc[recommended_shipping, recommended_payment]

    # Append results
    recommended_changes.append(
        {
            "order_id": order["order_id"],
            "current_shipping_mode": current_shipping_mode,
            "current_payment_type": current_payment_type,
            "recommended_shipping_mode": recommended_shipping,
            "recommended_payment_type": recommended_payment,
            "original_risk": order["late_delivery_risk"],
            "updated_shipping_risk": updated_shipping_risk,
            "updated_payment_risk": updated_payment_risk,
            "updated_both_risk": updated_both_risk,
        }
    )
    new_risk_scores_shipping.append(updated_shipping_risk)
    new_risk_scores_payment.append(updated_payment_risk)
    new_risk_scores_both.append(updated_both_risk)

# Create a DataFrame for recommendations
recommendations_df = pd.DataFrame(recommended_changes)

# Calculate % of late risk deliveries for each scenario
original_late_percentage = len(late_orders) / len(simulated_data) * 100
updated_shipping_late_percentage = (
    sum(np.array(new_risk_scores_shipping) >= optimal_threshold) / len(simulated_data) * 100
)
updated_payment_late_percentage = (
    sum(np.array(new_risk_scores_payment) >= optimal_threshold) / len(simulated_data) * 100
)
updated_both_late_percentage = (
    sum(np.array(new_risk_scores_both) >= optimal_threshold) / len(simulated_data) * 100
)

# Sort the recommendations DataFrame by original risk descending
recommendations_df = recommendations_df.sort_values(by="original_risk", ascending=False)

# Output results
st.subheader("Recommendations for Late Orders")
st.write("### Sorted Recommendations:")
st.dataframe(recommendations_df)

st.write("### Late Delivery Risk Percentages:")
st.write(f"- **Original Late Risk Deliveries**: {original_late_percentage:.2f}%")
st.write(f"- **% Late Risk Deliveries (Only Shipping Updated)**: {updated_shipping_late_percentage:.2f}%")
st.write(f"- **% Late Risk Deliveries (Only Payment Updated)**: {updated_payment_late_percentage:.2f}%")
st.write(f"- **% Late Risk Deliveries (Both Updated)**: {updated_both_late_percentage:.2f}%")

st.write("Overall recommendation is to update the payment type and shipping mode based on recommendation, otherwise prioritize the update of payment mode. Improve the payment infrastructure such that there are fewer transfer options, and more cash and debit payments. ")
