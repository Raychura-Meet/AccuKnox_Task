# ================================
# INSTALL LIBRARIES (Run once in Colab)
# ================================
!pip install requests pandas matplotlib

# ================================
# IMPORT LIBRARIES
# ================================
import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ================================
# FUNCTION: FETCH DATA FROM API (WITH FALLBACK)
# ================================
def fetch_data(url, fallback_data):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"Fetched data from API: {url}")
            return response.json()
        else:
            print(f"API failed ({response.status_code}), using fallback data.")
            return fallback_data
    except Exception as e:
        print(f"Error: {e}. Using fallback data.")
        return fallback_data


# ================================
# MAIN PROGRAM
# ================================
def main():
    # Use context manager for safe DB handling
    with sqlite3.connect("project.db") as conn:
        cursor = conn.cursor()

        # =====================================================
        # TASK 1: BOOKS API → SQLITE
        # =====================================================
        print("\n--- TASK 1: BOOKS API ---")

        books_fallback = [
            {"title": "Atomic Habits", "author": "James Clear", "year": 2018},
            {"title": "Deep Work", "author": "Cal Newport", "year": 2016},
            {"title": "Clean Code", "author": "Robert C. Martin", "year": 2008}
        ]

        books = fetch_data(
            "http://127.0.0.1:5000/books",  
            books_fallback
        )

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            author TEXT,
            year INTEGER
        )
        """)

        for book in books:
            cursor.execute("""
            INSERT OR IGNORE INTO books (title, author, year)
            VALUES (?, ?, ?)
            """, (book['title'], book['author'], book['year']))

        df_books = pd.read_sql_query("SELECT * FROM books", conn)
        print("\nBooks Data:")
        print(df_books)


        # =====================================================
        # TASK 2: STUDENTS API → AVG + VISUALIZATION
        # =====================================================
        print("\n--- TASK 2: STUDENT SCORES ---")

        students_fallback = [
            {"name": "Amit", "score": 85},
            {"name": "Neha", "score": 90},
            {"name": "Rohit", "score": 78},
            {"name": "Simran", "score": 88},
            {"name": "Karan", "score": 92}
        ]

        students = fetch_data(
            "http://127.0.0.1:5000/students",
            students_fallback
        )

        df_students = pd.DataFrame(students)

        avg_score = df_students['score'].mean()
        print(f"\nAverage Score: {avg_score:.2f}")

        # Visualization
        plt.figure()
        plt.bar(df_students['name'], df_students['score'])
        plt.axhline(avg_score, linestyle='--', label='Average Score')
        plt.title("Student Scores")
        plt.xlabel("Students")
        plt.ylabel("Scores")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()


        # =====================================================
        # TASK 3: CSV → SQLITE
        # =====================================================
        print("\n--- TASK 3: CSV TO DATABASE ---")

        df_csv = pd.DataFrame({
            "name": ["Karan", "Simran", "Amit", "Neha", "Rohit"],
            "email": [
                "karan@gmail.com",
                "simran@gmail.com",
                "amit@gmail.com",
                "neha@gmail.com",
                "rohit@gmail.com"
            ]
        })

        # Save CSV
        df_csv.to_csv("users.csv", index=False)

        # Create table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE
        )
        """)

        # Read CSV and insert efficiently
        df_read = pd.read_csv("users.csv")
        df_read.to_sql("users", conn, if_exists="append", index=False)

        df_users = pd.read_sql_query("SELECT * FROM users", conn)
        print("\nUsers Data:")
        print(df_users)


# ================================
# RUN PROGRAM
# ================================
if __name__ == "__main__":
    main()