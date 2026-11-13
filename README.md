# SQL & Pandas Translation Challenge

## Project Overview

This project demonstrates how to perform the same data analysis operations using SQL and Python's pandas library.

The objective is to understand the similarities and differences between relational database queries and DataFrame operations.

## Technologies Used

- Python
- pandas
- SQLite
- VS Code

## Dataset

The project uses a sample sales dataset containing eight records.

Each record includes:

- Product name
- Product category
- Unit price
- Quantity sold
- Sales quarter

The dataset is loaded into both an in-memory SQLite database and a pandas DataFrame.

## Questions Answered

1. What is the total revenue per product?
2. Which quarter had the highest total quantity sold?
3. What is the average unit price per category?
4. Which products had a total quantity greater than 200?

Each question is solved using both SQL and pandas.

## Bonus Feature

The project demonstrates using `pd.read_sql()` to execute a SQL query and return its results as a pandas DataFrame.

## Installation

**1. Clone the repository**

```powershell
git clone <repository-url>
cd translation-challenge
```

**2. Create a virtual environment**

```powershell
python -m venv .venv
```

**3. Activate the environment (Windows PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```powershell
python -m pip install -r requirements.txt
```

## Running the Application

Execute:

```powershell
python translation_challenge.py
```

The terminal displays the SQL and pandas results for each question.

## Project Structure

```text
translation-challenge/
├── .venv/
├── .gitignore
├── README.md
├── requirements.txt
└── translation_challenge.py
```

## Learning Outcomes

Through this project, I practiced:

- Loading data into SQLite and pandas
- Writing SQL queries using `GROUP BY`, `SUM`, `AVG`, and `HAVING`
- Using pandas `groupby()` and aggregation methods
- Comparing results between two data processing approaches
- Working with Python virtual environments
- Managing project dependencies

## Conclusion

This project demonstrates that SQL and pandas can accomplish many of the same data analysis tasks using different syntax and approaches. Understanding both tools provides flexibility when working with databases, datasets, and data-driven applications.
