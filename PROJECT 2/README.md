# DATA 201 — Project 2  
## Model Building, Evaluation, and Improvement (Regression Focus)

---

## Overview  

This is the second of two unit projects that you will complete this semester. Unit projects provide you with the opportunity to integrate concepts and techniques presented in the course. This project is intended to help you practice building, evaluating, and improving models in preparation for your final project.

The project is due on **[April 30]**. Late submissions will result in a reduction of points.

You will give a brief **3-5 minute presentation** of your project on **April 30** at the beginning of class.

This is an **individual project**. You may discuss ideas with classmates and use online resources for guidance, but your implementation, analysis, and interpretation must be your own work. You should be able to clearly explain your work if asked.

Please refer to the syllabus regarding **Data Science Integrity and AI Usage**.

---

## Project Goals  

In this project, you will:

- Explore and understand a real dataset  
- Build a baseline regression model  
- Improve the model using ideas from class  
- Evaluate model performance  
- Interpret results in context  
- Communicate your findings clearly  

---

## DATA  

Your dataset must:

- Contain **at least 2 quantitative variables** and **1 categorical variable**
- Contain at least **300–500 observations (recommended)**
- Include a **quantitative target variable** (required)

Additional rules:

- You may NOT reuse a dataset from a previous DATA course  
- You may NOT use the same dataset as another student  


---

## PROJECT SETUP  

- Use **Python (Jupyter Notebook / Google Colab)**  
- Submit via **MS Teams**  
- Upload all project files in **one folder** inside your **DATA 201 Team Repository**  

---

## Formatting Guidelines  

- Write explanations in **full sentences** (not code comments)  
- Use **Markdown cells** for explanations  
- Clearly label all plots and tables  
- Add short comments in code explaining key steps  

---

# Required Elements of Project 2 Report  

Each section should be **1–2 paragraphs** (excluding plots/tables).

---

## 1. Title  

Include:
- Project 2  
- DATA 201 Spring 2026  
- Your Name  
- Optional: Custom project title  

---

## 2. Introduction  

Provide a brief description of:

- Dataset source  
- Population of interest  
- Data collection method (if known)  
- Limitations of the data  
- Possible bias or ethical concerns  

Include a citation for your dataset.

---

## 3. Data Overview  

Describe your dataset:

- Number of rows and columns  
- What each row represents  
- Table of variables:
  - Name  
  - Type (quantitative/categorical)  
  - Description  

Include any data cleaning or transformations performed.

---

## 4. Data Analysis and Modeling  

This is the main part of your project.

---

### a. Data Exploration and Visualization  

Create and interpret **at least 3 visualizations**, such as:

- Histograms  
- Scatter plots  
- Boxplots  
- Bar charts  

Describe **patterns, relationships, or interesting observations**.

---

### b. Train/Test Split  

Split your data into:

- Training set  
- Testing set  

Explain your choice (e.g., 80/20 split).

---

### c. Build a Baseline Model  

Build a **linear regression model** using your selected variables.

Explain:

- What variables you included  
- Why you chose them  

---

### d. Improve Your Model  

Modify your model using at least **ONE** of the following:

- Transformation (log, polynomial, etc.)  
- Interaction term  
- Feature selection (adding/removing variables)  

You must:

- Explain **why** you made the change  
- Support your decision using:
  - plots  
  - patterns in the data  
  - model results  

---

### e. Compare Models  

Compare your baseline and improved models using appropriate metrics:

- RMSE  
- \(R^2\)

Clearly explain:

- Which model performs better  
- Why  

---

### f. Interpret Your Final Model  

Explain your regression model in plain language:

- Which variables are important?  
- What do the coefficients mean?  
- How do predictors affect the response variable?  

---

### g. Predictions  

Use your final model to:

- Make predictions for **3 new data points**  
- Interpret the results in context  

---

### (Optional) Classification Extension  

You may optionally:

- Build a classification model (e.g., logistic regression)  
- Compare it to your regression approach  

If included, you may report:

- Accuracy  
- ROC-AUC  

---

## 5. Conclusions and Recommendations  

Summarize:

- Key findings  
- Model performance  
- Any challenges or limitations  
- Whether your model generalizes well  
- Possible next steps or improvements  

If results are not strong or interesting, explain why.

---

## Submission Checklist  

Your submission must include:

- Jupyter Notebook (.ipynb)  
- All supporting files (data, images, etc.)  
- Organized in **one folder** inside your **DATA 201 Team Repository**  
- Submission link or confirmation via **MS Teams**  

---

## Grading Criteria  

| Component | Points |
|----------|--------|
| Correct implementation | 8 |
| Model improvement & reasoning | 6 |
| Interpretation & explanation | 4 |
| Organization & clarity | 2 |

**Total: 20 points**
