# DATA 201 --- Week 5 Assignment

## Resampling Methods with the Iris Dataset

In this assignment, we will explore **bootstrap resampling, jackknife
resampling, and permutation tests** using the **Iris dataset**.

The Iris dataset contains measurements of iris flowers from three
species:

-   *Setosa*
-   *Versicolor*
-   *Virginica*

Each flower has four measurements:

-   sepal length
-   sepal width
-   petal length
-   petal width

------------------------------------------------------------------------

# Load the Dataset

Use the following code to load the dataset.

``` python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

iris = sns.load_dataset("iris")
iris.head()
```

## Tasks

1.  Print the **number of observations** in the dataset.
2.  Print the **column names**.
3.  Count how many observations exist for each **species**.

------------------------------------------------------------------------

# Part 1 --- Bootstrap Resampling

We will estimate the **mean sepal length** using bootstrap resampling.

## Task 1 --- Basic Statistics

Compute the following statistics for **sepal length**:

-   mean
-   median
-   standard deviation

------------------------------------------------------------------------

## Task 2 --- Bootstrap the Mean

Perform **5,000 bootstrap resamples**.

Procedure:

1.  Sample the dataset **with replacement**.
2.  Each sample must contain **150 observations**.
3.  Compute the **mean sepal length** for each resample.
4.  Store the results.

Plot the **distribution of bootstrap means**.

**Note on Efficiency**

While 5,000 iterations is manageable for 150 rows, consider the
computational cost if our dataset had **1 million rows**.
If your computer feels slow, try **1,000 iterations first**.

------------------------------------------------------------------------

## Task 3 --- Confidence Interval

Using the bootstrap results, compute the **95% confidence interval**
using the percentile method:

CI = \[2.5%, 97.5%\]

Report:

-   Bootstrap mean
-   Lower bound
-   Upper bound

### Question

Why is it mathematically necessary to sample **with replacement** in
bootstrap resampling?

------------------------------------------------------------------------

# Part 2 --- Jackknife Resampling

## Task 4 --- Jackknife the Mean

Create jackknife samples by removing **one observation at a time**.

Steps:

1.  For each observation i, remove it from the dataset.
2.  Compute the mean of the remaining observations.
3.  Store the result.

Plot the **distribution of jackknife means**.

**Visualization Tip**

Because you are removing only **one data point at a time**, the
resulting means will be extremely similar.
You may need to:

-   use a **large number of bins**, or
-   adjust `plt.xlim()`

to clearly see the variation.

### Question

If the dataset contains n observations, **exactly how many jackknife
samples** are created?

------------------------------------------------------------------------

# Part 3 --- Permutation Test

We will test whether **sepal length differs significantly between two
species**.

For this task, use:

-   **Versicolor**
-   **Virginica**

## Task 5 --- Observed Statistic

Compute the observed difference in means:

difference = mean(Versicolor) − mean(Virginica)

------------------------------------------------------------------------

## Task 6 --- Permutation Simulation

Run **1,000 permutations**.

Procedure:

1.  Combine the two species into one dataset.
2.  **Shuffle (permute) the labels**.
3.  Split the data back into two groups of the original sizes.
4.  Compute the difference in means.
5.  Store the result.

Plot the **permutation distribution**.

------------------------------------------------------------------------

## Task 7 --- p-value

Compute the p-value:

p = (number of simulated differences ≥ observed difference) / (total
simulations)

Interpret the result at α = 0.05.

------------------------------------------------------------------------

## Questions

1.  What is the **null hypothesis (H0)** in this specific test?
2.  What does the **permutation distribution** represent in terms of
    **random chance**?
3.  Based on your p-value, do you **reject** or **fail to reject** the
    null hypothesis?

------------------------------------------------------------------------

# Submission

Submit a **Google Colab notebook** containing:

-   your code
-   plots
-   written answers

Then:

1.  Push your notebook to **GitHub** or simply upload if you do it in google colab.
2.  Submit the **GitHub link in MS Teams**.
