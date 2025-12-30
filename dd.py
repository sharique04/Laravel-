# topic_10_database_mysql.py
import mysql.connector
from mysql.connector import errorcode
import tkinter as tk
from tkinter import messagebox

# --- IMPORTANT: DATABASE CONFIGURATION ---
# Replace with your actual MySQL credentials.
# You must create the database 'school_db' manually in MySQL first.
# Example SQL command: CREATE DATABASE school_db;
config = {
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD',  # <--- CHANGE THIS
    'host': '127.0.0.1',
    'database': 'school_db',
}

# === PART 1: Console-based Student Table Operations ===

def db_connect():
    """Establishes a connection to the database."""
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist")
        else:
            print(f"Database connection error: {err}")
        return None

def create_students_table(cursor):
    """Creates the 'students' table."""
    try:
        cursor.execute("DROP TABLE IF EXISTS students")
        cursor.execute("""
            CREATE TABLE students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                marks INT
            )
        """)
        print("Table 'students' created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")

def insert_single_record(cursor, cnx):
    """Inserts one record."""
    try:
        sql = "INSERT INTO students (name, marks) VALUES (%s, %s)"
        val = ("Alice", 95)
        cursor.execute(sql, val)
        cnx.commit()
        print(f"1 record inserted, ID: {cursor.lastrowid}")
    except mysql.connector.Error as err:
        print(f"Insert failed: {err}")

def insert_multiple_records(cursor, cnx):
    """Inserts multiple records using executemany()."""
    try:
        sql = "INSERT INTO students (name, marks) VALUES (%s, %s)"
        vals = [("Bob", 88), ("Charlie", 72), ("Diana", 91)]
        cursor.executemany(sql, vals)
        cnx.commit()
        print(f"{cursor.rowcount} records were inserted.")
    except mysql.connector.Error as err:
        print(f"Insert multiple failed: {err}")

def update_student_marks(cursor, cnx):
    """Updates a student's marks."""
    try:
        sql = "UPDATE students SET marks = %s WHERE name = %s"
        val = (98, "Alice") # Update Alice's marks to 98
        cursor.execute(sql, val)
        cnx.commit()
        print(f"{cursor.rowcount} record(s) updated.")
    except mysql.connector.Error as err:
        print(f"Update failed: {err}")

def delete_student_record(cursor, cnx):
    """Deletes a student by name."""
    try:
        sql = "DELETE FROM students WHERE name = %s"
        val = ("Charlie",)
        cursor.execute(sql, val)
        cnx.commit()
        print(f"{cursor.rowcount} record(s) deleted.")
    except mysql.connector.Error as err:
        print(f"Delete failed: {err}")

def fetch_one_record(cursor):
    """Fetches a single record."""
    cursor.execute("SELECT id, name, marks FROM students WHERE name = 'Bob'")
    record = cursor.fetchone()
    print("\nFetching one record (Bob):")
    if record:
        print(record)
    else:
        print("Record not found.")

def fetch_all_records(cursor):
    """Fetches all records."""
    cursor.execute("SELECT id, name, marks FROM students")
    records = cursor.fetchall()
    print("\nFetching all records:")
    for row in records:
        print(row)

def run_student_db_operations():
    print("--- Running Console Student DB Operations ---")
    cnx = db_connect()
    if not cnx: return
    
    cursor = cnx.cursor()
    create_students_table(cursor)
    insert_single_record(cursor, cnx)
    insert_multiple_records(cursor, cnx)
    update_student_marks(cursor, cnx)
    delete_student_record(cursor, cnx)
    fetch_one_record(cursor)
    fetch_all_records(cursor)
    
    cursor.close()
    cnx.close()
    print("\n--- Console DB Operations Finished ---\n")

# === PART 2: Tkinter GUI Form for Book Details ===

class BookDBApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Entry Form")
        self.geometry("400x200")
        
        # Setup database table
        self.setup_database_table()
        
        # Create GUI elements
        self.create_widgets()

    def setup_database_table(self):
        cnx = db_connect()
        if not cnx: self.destroy(); return
        
        cursor = cnx.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    author VARCHAR(100) NOT NULL
                )
            """)
            print("Table 'books' is ready.")
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Failed to setup 'books' table: {err}")
        finally:
            cursor.close()
            cnx.close()

    def create_widgets(self):
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(expand=True)

        tk.Label(frame, text="Title:").grid(row=0, column=0, sticky="w", pady=5)
        self.title_entry = tk.Entry(frame, width=40)
        self.title_entry.grid(row=0, column=1)

        tk.Label(frame, text="Author:").grid(row=1, column=0, sticky="w", pady=5)
        self.author_entry = tk.Entry(frame, width=40)
        self.author_entry.grid(row=1, column=1)

        submit_button = tk.Button(frame, text="Add Book to Database", command=self.add_book)
        submit_button.grid(row=2, columnspan=2, pady=20)
        
    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()

        if not title or not author:
            messagebox.showwarning("Input Error", "Title and Author cannot be empty.")
            return

        cnx = db_connect()
        if not cnx: return

        cursor = cnx.cursor()
        try:
            sql = "INSERT INTO books (title, author) VALUES (%s, %s)"
            cursor.execute(sql, (title, author))
            cnx.commit()
            messagebox.showinfo("Success", f"Book '{title}' added to the database.")
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Failed to add book: {err}")
        finally:
            cursor.close()
            cnx.close()

if __name__ == "__main__":
    # Run the console part first
    run_student_db_operations()
    
    # Then, launch the GUI App
    print("--- Launching GUI Book Entry Form ---")
    app = BookDBApp()
    app.mainloop()
