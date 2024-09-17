# Bankruptcy Prediction Classification Model

This project focuses on predicting whether a company will remain solvent or go bankrupt based on financial factors. The model leverages machine learning techniques to classify companies using various financial indicators. The final model achieves an F1 score of 0.7 after processing with feature selection and imbalanced data handling techniques.

## Project Overview

Bankruptcy prediction is a crucial task in the financial domain, helping investors, creditors, and management assess the solvency risk of companies. The aim of this project is to develop a robust machine learning classification model to predict bankruptcy based on historical financial data.

## Dataset

The dataset used in this project contains financial indicators for various companies, with labels indicating whether the company went bankrupt. Initially, the data exhibited an imbalance ratio of 3.23% between solvent and bankrupt companies, requiring specialized techniques for handling this imbalance.

## Key Features

- **Optimal Model**: LGBM (LightGBM) Classifier
- **Evaluation Metric**: F1 Score
- **F1 Score Achieved**: 0.7
- **Data Imbalance Handling**: Resolved using **imblearn-oversampling**, which provided the best results.
- **Feature Selection**: Features were selected using **ModelReduceFeature** and **Recursive Feature Elimination (RFE)**.
- **Overfitting Check**: Multiple models were compared, and **RandomForest** exhibited overfitting, while **LGBMClassifier** performed optimally.
- **Techniques Used**: Data resampling, feature selection, and hyperparameter tuning.

## Models Tested

Several machine learning models were tested to identify the best performance in predicting bankruptcy:

- **RandomForestClassifier** (n_estimators = 10)
- **LogisticRegression** (solver = "liblinear", C = 9)
- **KNeighborsClassifier** (n_neighbors = 1, p = 2)
- **DecisionTreeClassifier** (max_depth = 30)
- **AdaBoostClassifier** (n_estimators = 60)
- **XGBClassifier** (min_child_weight = 1, max_depth = 6)
- **LGBMClassifier** (max_depth = 10)

Among all these models, the **LGBMClassifier** consistently outperformed others in terms of F1 score, train, and test accuracy, making it the final model selection for this project.

## Project Workflow

1. **Data Imbalance Handling**
   - The dataset was highly imbalanced with a 3.23% ratio of bankrupt companies.
   - Various resampling methods were evaluated, and **imblearn-oversampling** yielded the highest accuracy for resolving the imbalance.

2. **Feature Selection**
   - Feature selection techniques such as **Recursive Feature Elimination (RFE)** were applied across 4 classification models.
   - **ModelReduceFeature** and **LGBMClassifier** provided the best combination for optimal accuracy.

3. **Model Development**
   - After testing multiple models, **LGBMClassifier** was chosen as the best-performing model.
   - **RandomForestClassifier** exhibited overfitting, while hyperparameter tuning on other models did not improve performance.
   - **LGBMClassifier** performed well in both train and test phases, offering the highest F1 score.

4. **Final Model**
   - The final model was built using:
     - **Resampling Method**: imblearn-oversampling
     - **Feature Selection**: ModelReduceFeature
     - **Model**: LGBMClassifier

5. **Model Evaluation**
   - The model was evaluated using precision, recall, accuracy, and F1 score, with the best F1 score achieved being **0.7**.

## Tools and Technologies Used

- **Language**: Python
- **Libraries**: Scikit-learn, XGBoost, Imbalanced-learn (imblearn), Pandas, NumPy
- **Development Environment**: Jupyter Notebooks, VS Code, Whimsical, GitHub
- **Evaluation Metrics**: F1 Score, Precision, Recall, Accuracy
- **Techniques**: Data resampling, feature selection, and hyperparameter tuning

## Future Work
- **Data Expansion**: Expand the dataset to include more financial indicators and different time periods for robustness.
- **Model Explainability**: Use SHAP (SHapley Additive exPlanations) values to interpret model predictions and explain the model's decision-making process.

## Conclusion

This project successfully demonstrates the use of machine learning techniques to predict bankruptcy with an F1 score of 0.7. By addressing data imbalance through oversampling, performing feature selection, and identifying the best model (LGBMClassifier), the project offers a robust solution for bankruptcy prediction.

## Contributors

Developed by Divya Khanolkar, Chi Wen Lee & Yunhan Chiu.