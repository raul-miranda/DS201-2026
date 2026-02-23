# Assignment 2 – Data Wrangling with pandas
*(Based on Class 2 – pandas for R users)*

---

## Learning Objectives
By completing this assignment, you should be able to:

- Use pandas equivalents of `dplyr` verbs:
  - `filter()` → boolean indexing / `.loc[]`
  - `mutate()` → `.assign()`
  - `group_by()` → `.groupby()`
  - `summarise()` → `.agg()`
  - `arrange()` → `.sort_values()`
- Apply boolean logic correctly using `&` and `|`
- Use **method chaining** for readable, step-by-step transformations
- Create grouped summary tables with multiple statistics

---

## Dataset

Use the provided dataset: `housing.csv`

```python
import pandas as pd
df = pd.read_csv("housing.csv")
```

---

# Part A – Core Wrangling (Method Chaining Required)

Using **one chained expression**, create a summary table that:

1. Keeps only observations where `price > 250000`
2. Keeps only homes with `size > 1000`
3. Creates a new variable:
   - `price_per_sqft = price / size`
4. Groups by `neighborhood`
5. Computes:
   - mean of `price_per_sqft`
   - median of `price_per_sqft`
   - count of homes
6. Sorts the result by mean `price_per_sqft` (descending)

### Requirements
- Do NOT create intermediate variables (`df2`, `df3`, etc.)
- Use `.assign()` to create new variables
- Use `.agg()` with named aggregation
- **Do not use `reset_index()`** (we did not cover it yet)

### Output format note
After `groupby()`, pandas will put `neighborhood` in the *index*. That is OK for this assignment.
Your final output can look like a table where `neighborhood` is on the left as the index.

### Deliverable
- Paste your code
- Show the final DataFrame output

---

# Part B – Translation to dplyr

In a Markdown cell, write the equivalent **dplyr** code that performs the same transformation.

Your R pipeline should include:

- `filter()`
- `mutate()`
- `group_by()`
- `summarise()`
- `arrange()`

### Reflection (3–6 sentences)

Answer:

- Which syntax feels clearer for you — pandas chaining or dplyr pipelines?
- What feels similar between them?
- What feels different?

---

# Part C – Boolean Logic Debugging

The following code produces an error:

```python
df[df["price"] > 250000 & df["size"] > 1000]
```

### Tasks

1. Fix the code.
2. Explain **why** the error occurs.
3. Rewrite the filter using `.query()` instead.

---

# Part D – Short Concept Questions

Answer briefly (2–4 sentences each):

1. Why must we wrap each condition in parentheses when using `&` in pandas?
2. What is the advantage of method chaining over creating many temporary DataFrames?
3. In `.agg(mean_price=("price", "mean"))`, what does `"price"` represent? What does `"mean"` represent?
4. When you `groupby("neighborhood")`, why does `neighborhood` appear on the left (index) in the result table?

---

## Optional Extension (Extra practice)
Create a second summary table grouped by `type` that reports:
- mean `price`
- median `price`
- count of listings
(Use method chaining again.)
