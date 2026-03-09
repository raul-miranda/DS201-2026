
# Assignment – Week 4  
## Logistic Regression: R → Python Bridge

**Course:** Data Science  
**Submission:** Jupyter Notebook (.ipynb)  
**Dataset:** `housing.csv`

---

# Learning Objectives

By the end of this assignment, you should be able to:

- Fit and interpret **logistic regression models**
- Translate workflows from **R (glm / tidymodels)** to **Python**
- Interpret **odds ratios**
- Evaluate classification models using **Accuracy and ROC–AUC**
- Reflect on the difference between **statistical inference vs prediction**

---

# Dataset Description

The dataset contains **600 housing listings**.

| Variable | Description |
|---|---|
| listing_id | Unique identifier |
| price | Sale price of the house |
| size | House size (square footage) |
| bedrooms | Number of bedrooms |
| neighborhood | Location category |
| type | Housing type (SingleFamily, Townhouse, MultiFamily) |

---

# Step 0 – Create a Binary Outcome

For classification, convert price into a binary variable.

```
high_price = price > median(price)
```

This creates two groups:

- `1` → expensive homes  
- `0` → less expensive homes  

---

# Part A – Logistic Regression for Inference



### In Python

Fit the equivalent model using **statsmodels**.

Example:

```python
import statsmodels.formula.api as smf

model = smf.logit(
    "high_price ~ size + bedrooms + C(neighborhood)",
    data=df
).fit()

print(model.summary())
```

### Report

Create a table including:

- coefficients
- odds ratios
- p-values

Odds ratios:

```
odds_ratio = exp(coefficient)
```

### Short Analysis

Answer:

- Which predictors appear **statistically significant**?
- Which neighborhood has **higher odds** of expensive homes?

---

# Part B – Interpretation (Plain Language)

Choose **one variable** and explain its odds ratio.

Example:

> “For every additional bedroom, the odds of a house being expensive increase by ___.”

Your explanation should be understandable to someone **without statistics training**.

---

# Part C – Prediction Workflow  
## (tidymodels → scikit-learn)

### 1. Train/Test Split

Split the data:

- 80% training
- 20% testing

Example:

```python
from sklearn.model_selection import train_test_split
```

### 2. Fit Logistic Regression

Use:

```
sklearn.linear_model.LogisticRegression
```

Encode categorical variables such as:

```
neighborhood
type
```



### 3. Evaluate the Model ( check slides for more info about this)

Report:

- **Accuracy**
- **ROC–AUC**

Useful functions:

```
sklearn.metrics.accuracy_score
sklearn.metrics.roc_auc_score
```

Optional: plot an ROC curve.

---

# Part D – Model Understanding

### Accuracy vs AUC

Why might **ROC–AUC** sometimes be preferred over **accuracy**?

Explain in **2–3 sentences**.

### Inference vs Prediction

Which modeling approach would you choose for:

- **Policy analysis**
- **Prediction tasks**

Explain why.

---

# Part E – Explore the Dataset

Before modeling, briefly explore the data.

Create **at least three plots** such as:

- Histogram of `price`
- Scatter plot: `size` vs `price`
- Boxplot: `price` by `neighborhood`
- Bar chart: housing `type`

Discuss **one interesting pattern** you observe.

---

# Deliverables

Your notebook should include:

1. Data loading
2. Data exploration plots
3. Logistic regression (statsmodels)
4. Odds ratio interpretation
5. scikit-learn prediction workflow
6. Evaluation metrics
7. Reflection answers

---

# Grading Rubric

| Component | Points |
|---|---|
| Correct implementation | 8 |
| Conceptual explanation | 6 |
| Code clarity and organization | 4 |
| Reflection and insight | 2 |

Total: **20 points**

---
