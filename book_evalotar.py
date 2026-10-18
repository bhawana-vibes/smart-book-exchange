import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="enter the password",  
        database="book_exchange"
    )
def get_resale_price(class_grade , mrp ,condition):
        if class_grade < 9 or class_grade > 12:
            return "Invalid class"
        if condition.lower() == "Good":
            rate = 0.50
        else:
            rate = 0.40

        fair_price = mrp * rate
        return fair_price

def save_to_database(title, grade, mrp, cond, resale):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO books (book_title, class_grade, mrp, book_condition, resale_price)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (title, grade, mrp, cond, resale)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()
    print(f"'{title}' database is save permanently")
all_books = []
while(True):
    print("/n---- new book list ----")
    Title = input("enter the book name:")
    Grade = int(input("Enter the class(9-12):"))
    Price = float(input("enter the price:"))
    Cond = input("enter the condition(good/average):")
    
#print(get_resale_price(10, 500, "Good"))
#print(get_resale_price(7, 300, "Good"))
    result = get_resale_price(Grade, Price, Cond)
    print("Fair Resale Price:", result)
    result = get_resale_price(Grade, Price, Cond)
    print("Fair Resale Price:", result)
    if result != "Invalid class":
        all_books.append({
            "title": Title,
            "class": Grade,
            "mrp": Price,
            "resale": result
        })
        save_to_database(Title, Grade, Price, Cond, result)
    else:
        print("Add no this book becacuse this is invalid class.")
    choice = input("Add the other books(yes/no):").lower()
    if choice != "yes":
         break
print("\nall books list")
print(all_books)

import pandas as pd
df = pd.DataFrame(all_books)
print("/n---- Book Table -----")
print(df)
total_mrp = df['mrp'].sum()
total_resale = df['resale'].sum()
total_savings = total_mrp - total_resale

print(f"\nTotal MRP: ₹{total_mrp}")
print(f"Total Fair Price: ₹{total_resale}")
print(f"Total Student Savings: ₹{total_savings}")

if all_books:
    df = pd.DataFrame(all_books)
    print("\n--- Books Summary (Pandas DataFrame) ---")
    print(df)

conn = get_connection()
query = "SELECT * FROM books WHERE status = 'AVAILABLE'"

db_df = pd.read_sql(query, conn)
conn.close()

print("\n--- Live Data from MySQL Database (Pandas) ---")
print(db_df)