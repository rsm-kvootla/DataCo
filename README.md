# DataCo - Sport Retail Client
Late Delivery Risk Prediction for a sport retail client of DataCo

# Project Overview

This project, titled "Identifying Risk of Late Deliveries in a Sports Retail Business," focuses on analyzing and mitigating late deliveries in a sports retail business operating across the Americas. The business fulfills over 21,000 orders annually, generating $42 million in sales, with products sourced from the USA and Puerto Rico and sold across 22 countries.

# Problem Statement

- 57% of the deliveries are late, with no improvement in late delivery rates over the past three years.
- While 45% of late deliveries are attributed to orders sent to Central America, late delivery rates remain consistent across regions.

# Objectives

1. Identify key variables influencing late deliveries.
2. Develop predictive models to flag high-risk orders.
3. Provide actionable recommendations to improve delivery performance.

# Methodology
Data Analysis:

Variables such as payment type, shipping mode, dispatch location, and order status were analyzed.
Chi-square tests identified significant variables affecting late deliveries: shipping mode, order country, customer state, and payment type.

Model Development:
Logistic regression was chosen for its interpretability and feature significance.
Features: shipping_mode, type, and order_country.
Evaluation Metrics: Precision, Recall, F1-Score, and ROC AUC.

Dashboards:
Developed two interactive Streamlit dashboards for operational insights:
Dashboard 1: High-level overview for executives.
Dashboard 2: Order-level insights for analysts.

# Key Insights

Shipping Mode:
First Class: 0% late deliveries.
Standard Class: Highest late rate at 59.9%.

Geographic Trends:
Guyana and Costa Rica have the highest late delivery rates (>69%).
French Guiana has the lowest rate (33.33%).

Recommendations:
Optimize shipping methods for time-sensitive deliveries.
Improve payment processing systems.
Explore stocking products in regional hubs to minimize delays.

# Deliverables
Predictive Model:
Achieved an F1-Score of 0.8021 and an accuracy of 69%.
Successfully flags 53.69% of late deliveries while minimizing false positives.

Interactive Dashboards:
Visualize late delivery risks by country, shipping mode, and payment type.
Provide recommendations at the order level based on simulated data.

# Future Scope
Collect additional data on local regulations and alternate delivery routes.
Investigate why premium shipping options are less efficient.
Expand predictive models to include more variables for improved accuracy.


# For more details, refer to the full report and dashboards:
- latedeliverydashboard.streamlit.app/
- Sport Retail DataCo.pdf

To execute files:
1. Data file - datanew2.csv
2. Variable decision - Picking Variables.ipynb
3. Model decision - Picking the right model.ipynb
4. Final model - finalmodel2.pkl
5. Streanlit app files - streamlitlatedeliveryrisk.py, requirements.txt
