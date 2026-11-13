"""SQL and pandas translation challenge.

Run with: python translation_challenge.py
Dependency: pandas (install with: python -m pip install pandas)
"""

import sqlite3
import pandas as pd


sales_data = [
    ("Widget A", "Electronics", 29.99, 150, "2025-Q1"),
    ("Widget B", "Electronics", 49.99, 89, "2025-Q1"),
    ("Gadget X", "Accessories", 15.99, 300, "2025-Q1"),
    ("Widget A", "Electronics", 29.99, 200, "2025-Q2"),
    ("Gadget Y", "Accessories", 22.99, 175, "2025-Q2"),
    ("Widget C", "Electronics", 79.99, 50, "2025-Q2"),
    ("Gadget X", "Accessories", 15.99, 280, "2025-Q2"),
    ("Widget B", "Electronics", 49.99, 120, "2025-Q3"),
]
COLUMNS = ["product", "category", "unit_price", "quantity", "quarter"]


def display_comparison(title, sql_result, pandas_result):
    """Show two equivalent solutions and confirm they agree."""
    print(f"\n{title}")
    print("SQL result:")
    print(sql_result.to_string(index=False))
    print("\npandas result:")
    print(pandas_result.to_string(index=False))
    pd.testing.assert_frame_equal(
        sql_result.reset_index(drop=True),
        pandas_result.reset_index(drop=True),
        check_dtype=False,
        check_exact=False,
        atol=1e-8,
    )
    print("MATCH: SQL and pandas agree.")


def main():
    # Load the same source data into a pandas DataFrame and an in-memory SQLite database.
    df = pd.DataFrame(sales_data, columns=COLUMNS)
    with sqlite3.connect(":memory:") as conn:
        conn.execute("""
            CREATE TABLE sales (
                product TEXT, category TEXT, unit_price REAL,
                quantity INTEGER, quarter TEXT
            )
        """)
        conn.executemany(
            "INSERT INTO sales (product, category, unit_price, quantity, quarter) "
            "VALUES (?, ?, ?, ?, ?)",
            sales_data,
        )

        # QUESTION 1: What is the total revenue (unit_price * quantity) per product?
        # SQL: SUM(expression) + GROUP BY
        q1_sql = """
            SELECT product, ROUND(SUM(unit_price * quantity), 2) AS total_revenue
            FROM sales
            GROUP BY product
            ORDER BY product
        """
        sql_1 = pd.read_sql_query(q1_sql, conn)
        # pandas: assign calculated row revenue, then groupby + sum
        pandas_1 = (
            df.assign(revenue=df["unit_price"] * df["quantity"])
            .groupby("product", as_index=False)["revenue"].sum()
            .rename(columns={"revenue": "total_revenue"})
            .sort_values("product")
            .reset_index(drop=True)
        )
        pandas_1["total_revenue"] = pandas_1["total_revenue"].round(2)
        display_comparison("Q1. Total revenue per product", sql_1, pandas_1)

        # QUESTION 2: Which quarter had the highest total quantity sold?
        # SQL: GROUP BY + SUM + ORDER BY descending + LIMIT 1
        q2_sql = """
            SELECT quarter, SUM(quantity) AS total_quantity
            FROM sales
            GROUP BY quarter
            ORDER BY total_quantity DESC, quarter ASC
            LIMIT 1
        """
        sql_2 = pd.read_sql_query(q2_sql, conn)
        # pandas: groupby + sum + sort + head(1)
        pandas_2 = (
            df.groupby("quarter", as_index=False)["quantity"].sum()
            .rename(columns={"quantity": "total_quantity"})
            .sort_values(["total_quantity", "quarter"], ascending=[False, True])
            .head(1).reset_index(drop=True)
        )
        display_comparison("Q2. Quarter with highest quantity sold", sql_2, pandas_2)

        # QUESTION 3: What is the average unit price per category?
        # This is an unweighted average of the listed rows, not weighted by quantity.
        # SQL: AVG + GROUP BY
        q3_sql = """
            SELECT category, ROUND(AVG(unit_price), 2) AS average_unit_price
            FROM sales
            GROUP BY category
            ORDER BY category
        """
        sql_3 = pd.read_sql_query(q3_sql, conn)
        # pandas: groupby + mean
        pandas_3 = (
            df.groupby("category", as_index=False)["unit_price"].mean()
            .rename(columns={"unit_price": "average_unit_price"})
            .sort_values("category").reset_index(drop=True)
        )
        pandas_3["average_unit_price"] = pandas_3["average_unit_price"].round(2)
        display_comparison("Q3. Average unit price per category", sql_3, pandas_3)

        # QUESTION 4: Which products sold MORE THAN 200 units across all quarters?
        # SQL: GROUP BY + HAVING (filter aggregate groups)
        q4_sql = """
            SELECT product, SUM(quantity) AS total_quantity
            FROM sales
            GROUP BY product
            HAVING SUM(quantity) > 200
            ORDER BY product
        """
        sql_4 = pd.read_sql_query(q4_sql, conn)
        # pandas: groupby + sum + boolean filter
        pandas_4 = (
            df.groupby("product", as_index=False)["quantity"].sum()
            .rename(columns={"quantity": "total_quantity"})
            .query("total_quantity > 200")
            .sort_values("product").reset_index(drop=True)
        )
        display_comparison("Q4. Products with total quantity over 200", sql_4, pandas_4)

        # BONUS: pd.read_sql() executes SQL and directly returns a pandas DataFrame.
        bonus_df = pd.read_sql(q1_sql, conn)
        print("\nBONUS: pd.read_sql() result for Q1:")
        print(bonus_df.to_string(index=False))

    print("\nAll four SQL/pandas comparisons passed.")


if __name__ == "__main__":
    main()
