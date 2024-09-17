# Bitcoin Prices & CO2 Emissions Analysis

## Overview

This project explores the relationship between Bitcoin prices and CO2 emissions resulting from Bitcoin mining activities. It leverages historical data and statistical methods to analyze this relationship, focusing on key features affecting CO2 emissions.

## Scope of Analysis

- **Bitcoin Prices**: Historical data on Bitcoin prices.
- **CO2 Emissions**: Data on CO2 emissions from Bitcoin mining activities.

### Key Exclusions

- **E-Waste Generation**: Although significant, e-waste generation from cryptocurrencies is not covered in this analysis.

## Methodology

1. **Data Preparation**:
    - Selected useful features related to Bitcoin mining and emissions.
    - Scaled the features to standardize the data.

2. **Modeling**:
    - **Model**: Used XGBoost Regressor to model the relationship between features and CO2 emissions.
    - **Hyperparameter Tuning**: Applied Bayesian Optimization to find the optimal hyperparameters for the XGBoost model.

3. **Evaluation**:
    - Evaluated the model using Mean Squared Error (MSE), Mean Absolute Error (MAE), and R² Score on both training and testing sets.
    - Analyzed feature importance to understand the impact of different features on CO2 emissions predictions.

## Visualizations

The following visualizations were generated:

- **Historical Bitcoin Prices**: Trends and patterns in Bitcoin prices over time.
- **Bitcoin Halving Events**: Impact of Bitcoin halving events on hash rate.
- **Number of Bitcoins Created**: Visualization of the number of Bitcoins created over time.
- **Price vs CO2 Emissions**: Relationship between Bitcoin prices and CO2 emissions from mining activities.
- **Energy Consumed by Bitcoin**: Visualization of the energy consumption associated with Bitcoin mining.

## Key Findings

- **Feature Importance**: 
    - **Most Important Features**: Power required to mine Bitcoin and energy consumed per day by the Bitcoin network. These features are crucial as they directly impact the environmental footprint of Bitcoin mining.
    - **Less Important Features**: Price of Bitcoin, number of coins created, and block time. These features, while reflecting market dynamics and technical aspects, have a relatively lesser impact on CO2 emissions.
    - **Energy Efficiency**: Energy efficiency was found to be the least important feature in terms of its influence on Bitcoin’s performance or value.

- **Correlation**: There is a moderately positive correlation between Bitcoin prices and CO2 emissions from mining activities, indicating that changes in Bitcoin prices tend to coincide with changes in CO2 emissions.

- **Influencing Factors**: The relationship between Bitcoin prices and CO2 emissions is influenced by various factors, including technological advancements, regulatory developments, and market dynamics.

- **Environmental Impact**: The findings underscore the importance of addressing the environmental impact of cryptocurrency mining through sustainable practices and regulatory interventions. The model highlights the significant role of network hashrate and power consumption as primary drivers of CO2 emissions, suggesting the need for urgent measures to mitigate Bitcoin mining's environmental impact.

- **Comparative Analysis**: The environmental toll of Bitcoin mining, relative to its market value, is comparable to that of traditional gold mining. This emphasizes the need for sustainable practices and regulatory measures in the cryptocurrency industry.

## Tools and Technologies Used

- **Language**: Python
- **Libraries**: 
  - `pandas` for data manipulation
  - `numpy` for numerical operations
  - `matplotlib` for plotting
  - `xgboost` for modeling
  - `skopt` for hyperparameter tuning
  - `scikit-learn` for machine learning utilities
- **Development Environment**: Jupyter Notebooks, VS Code, GitHub, PowerBI
- **Evaluation Metrics**: Mean Absolute Error (MAE), Mean Squared Error (MSE), R² Score
- **Techniques**: 
  - Bayesian Optimization for hyperparameter tuning
  - Feature Importance Analysis
  - Learning Curves for model performance visualization

## Contributors

Developed by Divya Khanolkar, Mohammad Tayyab, Suman Sarawad & Sarthak Kinger


