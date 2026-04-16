# Week 9: Cross-Validation, Regularization & Optimization  
## How Do We Trust Models?

---

## Class 8a: Model Evaluation & Trust

### Topics
- Train/Test Split  
- Cross-Validation  
- Bootstrap (Conceptual Overview)  
- Bias–Variance Tradeoff  
- Honest Performance Estimation  

### Learning Objectives
By the end of this class, students will be able to:
- Explain why training error alone is misleading  
- Use resampling methods to estimate generalization performance  
- Describe the relationship between model complexity, bias and variance  
- Apply evaluation techniques consistently across different model types  

---

## Class 8b: Automated Complexity Control

### Topics
- Ridge, Lasso, and Elastic Net  
- Loss Functions with Penalties  
- Hyperparameter Tuning using Cross-Validation  
- Stability vs. Sparsity  
- Manual Feature Selection vs. Regularization  

### Learning Objectives
By the end of this class, students will be able to:
- Explain how regularization controls model complexity  
- Compare shrinkage-based and selection-based approaches  
- Interpret regularized model coefficients conceptually  
- Connect regularization methods to earlier feature selection decisions  

---

## Big Idea of the Week
Good models are not just accurate on training data; they generalize well.  
This week focuses on how to measure trust in a model and how to control complexity to avoid overfitting.

---

## Suggested Workflow for Students
1. Train a model  
2. Evaluate using cross-validation  
3. Tune hyperparameters  
4. Compare models (with and without regularization)  
5. Interpret results, not just accuracy  
