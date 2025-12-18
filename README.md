### **AIGuard: AI-Driven Grey Market \& Anomaly Detection**



*Predicting Revenue Leakage \& Unauthorized Distribution in Global Retail*



##### **📌 Project Overview**

AIGuard is an end-to-end machine learning solution designed to detect Grey Market (Parallel Import) activities. By analyzing over 500,000 global transactions, the system identifies unauthorized "bulk dumping" and significant price erosion that can cannibalize brand revenue.



###### **📊 Key Insights \& Visualizations**

Price Variance Index (PVI): Our engineered metric reveals that 5% of the market operates at discounts exceeding 60%, a major red flag for unauthorized sales.



Geographic Hotspots: The model identified the UK, Netherlands, and Australia as high-risk hubs for price erosion.



Wholesale Leakage: Scatter plots clearly distinguish "Normal Retail" from "Unauthorized Wholesale" clusters (High Volume + Deep Discount).



###### **🧠 The AI Pipeline**

Data Ingestion: Processed the UCI Online Retail II dataset (multinational transactional logs).



Feature Engineering: Calculated PVI to normalize price deviations across different products and currencies.



Model: Deployed an Unsupervised Isolation Forest algorithm to isolate outliers without requiring pre-labeled fraud data.



Inference: Serialized the model into a .joblib artifact for real-time risk scoring.



###### **🚨 Real-Time Detection**

Our Colab-based Inference Simulator allows users to input new transactions and receive an instant risk assessment.



Example Alert: "Suspicious Transaction Found: 1,200 units of 'Medium Ceramic Top Jar' flagged at 64% discount."



###### **🚀 Strategic Recommendations**

Supply Chain Forensic: Perform deep-dives into wholesalers moving high-risk SKUs like "Heart Card Holders".



Global Price Alignment: Harmonize MSRPs across leaky borders to eliminate the incentive for "Geographic Arbitrage".



Tracking: Implement unique serial number tracking for top-flagged products to trace leakage back to the source.

