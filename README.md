A strong technical summary bridges the gap between raw code and business value. You should structure it to highlight the Pipeline Architecture.

Project: AIGuard - Grey Market Detection Pipeline
Technical Overview: Our solution implements an unsupervised machine learning pipeline to identify unauthorized "Grey Market" transactions within global retail logs. By shifting from rule-based filters to anomaly isolation, we detect subtle "Parallel Trade" patterns that manual auditing misses.

Pipeline Stages:

Data Ingestion: Automated cleaning of 500k+ records from the UCI Online Retail II dataset, handling multinational currencies and wholesale noise.

Feature Engineering: Introduction of the Price Variance Index (PVI), a normalized metric calculating the percentage deviation of UnitPrice from a median-derived MSRP baseline.

Anomaly Detection: Deployment of an Isolation Forest ensemble. The model isolates outliers by measuring the "path length" required to separate a data point in a random tree structure.

Persistence & Serving: The trained model is serialized as a .joblib artifact for lightweight, real-time inference.
