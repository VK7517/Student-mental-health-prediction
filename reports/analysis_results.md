# Mental Health Analysis & Classification Project - Research Notes

This document provides a comprehensive overview of the **Mental Health screening and classification project** located at `d:/ML_Projects/Mental_Health`.

## Codebase Directory Structure
The workspace is organized as follows:
- [Models/](file:///d:/ML_Projects/Mental_Health/Models): Serialized machine learning models (`Descision_Tree_CLassifier.pkl`, `Gradient_Boosting_Classifier.pkl`, `Logistic_Regression.pkl`, `Random_Forest_Classifier.pkl`, `SVM_Classifier.pkl`, `label_encoder.pkl`).
- [dashboard/](file:///d:/ML_Projects/Mental_Health/dashboard): Power BI dashboard `Mental Health Analysis Dashboard.pbix`.
- [data/](file:///d:/ML_Projects/Mental_Health/data): Datasets directory, with raw input files in `data/raw/` and cleaned datasets in `data/cleaned/`.
- [notebook/](file:///d:/ML_Projects/Mental_Health/notebook): Jupyter notebooks detailing data cleaning, clustering, EDA, and model training.
- [reports/](file:///d:/ML_Projects/Mental_Health/reports): Model evaluation summaries, tables, and visualization charts.
- [src/](file:///d:/ML_Projects/Mental_Health/src): Python source code for data preprocessing, clustering rules, and helper evaluation functions.

---

## 1. Datasets & Data Cleaning
- **Raw Data:** [MentalHealthScreeningTest_Report_AllEntries.csv](file:///d:/ML_Projects/Mental_Health/data/raw/MentalHealthScreeningTest_Report_AllEntries.csv) contains 3,258 records and 54 columns representing survey responses from GHQ, DASS, and BRS mental health tests.
- **Feature Selection:** A subset of 8 relevant features is extracted: `["Age", "Gender", "Branch", "GHQ Score", "Total Score (DASSD-I)", "Total Score (DASSD-II)", "Total Score (DASSD-III)", "BRS Score"]`.
- **Cleaning Actions:**
  - Capped and cleaned out-of-range Age outliers to 18.
  - Renamed columns to cleaner formats: `Age`, `Gender`, `Branch`, `GHQ`, `Depression`, `Anxiety`, `Stress`, `BRS`.
  - Saved the processed dataset to [processing.csv](file:///d:/ML_Projects/Mental_Health/data/cleaned/processing.csv).

---

## 2. Rule-Based Cluster Assignment
A custom rule-based classification algorithm assigns subjects to clusters `A` through `H` (or `Unclassified`) based on clinical threshold categories:
- **Depression levels:**
  - $\le 9$: Normal
  - $10$ to $13$: Mild
  - $14$ to $20$: Moderate
  - $\ge 21$: Severe/Extremely Severe
- **Anxiety levels:**
  - $\le 7$: Normal
  - $8$ to $9$: Mild
  - $10$ to $14$: Moderate
  - $\ge 15$: Severe/Extremely Severe
- **Stress levels:**
  - $\le 14$: Normal
  - $15$ to $18$: Mild
  - $19$ to $25$: Moderate
  - $\ge 26$: Severe/Extremely Severe
- **BRS levels (Brief Resilience Scale):**
  - $0.0$: Balanced wellbeing
  - $< 3.0$: Low
  - $\le 4.3$: Average
  - $> 4.3$: High
- **Cluster Logic Rules ([cluster_formation.py](file:///d:/ML_Projects/Mental_Health/src/cluster_formation.py)):**
  - **Cluster A:** $GHQ < 12$
  - **Cluster E:** Severe condition present & BRS = High
  - **Cluster F:** Severe condition present & BRS = Low
  - **Cluster G:** $GHQ \ge 12$ & Depression/Anxiety/Stress $\le$ Mild & BRS = Low
  - **Cluster B:** $12 \le GHQ$ & Depression/Anxiety/Stress $\le$ Mild & BRS $\in$ [Average, High]
  - **Cluster H:** $GHQ \ge 12$ & Exactly one moderate domain & No severe domains & BRS = Low
  - **Cluster C:** Exactly one moderate domain & BRS $\in$ [Average, High]
  - **Cluster D:** Two or more moderate domains & BRS $\in$ [Low, Average]
  - **Unclassified:** Default fallback.

---

## 3. Modeling and Evaluation Results
The target variable is the assigned `Cluster` (which is mapped to class label indexes using a Scikit-Learn `LabelEncoder`). 

### Preprocessing Pipeline ([preprocessing.py](file:///d:/ML_Projects/Mental_Health/src/preprocessing.py))
- Numerical variables (`GHQ`, `Depression`, `Anxiety`, `Stress`, `BRS`) are normalized using `StandardScaler`.
- Categorical variables (`Gender`) are encoded using `OneHotEncoder(handle_unknown='ignore')`.

### Model Evaluation Table ([Evaluation_Metrics_Table.csv](file:///d:/ML_Projects/Mental_Health/reports/Evaluation_Metrics_Table.csv))

| Model | Accuracy | Precision (Macro) | Recall (Macro) | F1-Score (Macro) |
| :--- | :---: | :---: | :---: | :---: |
| **XGBoost (Gradient Boosting)** | **99.85%** | **87.17%** | **87.50%** | **87.33%** |
| **Decision Tree** | 99.69% | 86.86% | 87.27% | 87.06% |
| **Random Forest** | 99.54% | 86.56% | 87.05% | 86.78% |
| **SVM** | 96.93% | 81.60% | 80.58% | 81.06% |
| **Logistic Regression** | 94.02% | 73.74% | 67.11% | 68.59% |

*Note: Macro Recall scores are lower than Accuracy because some rare target clusters (like Cluster E, which contains only 4 samples out of 3,258 records) suffer from extreme class imbalance.*
