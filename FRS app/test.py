import sqlite3
import hashlib

# Connect to SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS admin
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT  NOT NULL,
              password TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL,
              mobile TEXT NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS faculty
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT  NOT NULL,
              password TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL,
              mobile TEXT NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS student
             (id TEXT PRIMARY KEY NOT NULL ,
              username TEXT  NOT NULL,
              password TEXT NOT NULL,
              email TEXT NOT NULL,
              mobile TEXT NOT NULL)''')
conn.commit()
c.execute("DELETE FROM student WHERE id = ?", ('y20acs841',))
def register_user(type,id,username, password, email, mobile):
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Insert user data into the database
    if type=="admin":
        try:
            c.execute('''INSERT INTO admin (username, password, email, mobile)
                        VALUES (?, ?, ?, ?)''', (username, hashed_password, email, mobile))
            conn.commit()
        except:
            print("User Already Exists")
    elif type=="faculty":
        try:
            c.execute('''INSERT INTO faculty (username, password, email, mobile)
                        VALUES (?, ?, ?, ?)''', (username, hashed_password, email, mobile))
            conn.commit()
        except:
            print("User Already Exists")
    elif type=="student":
        try:
            c.execute('''INSERT INTO student (id,username, password, email, mobile)
                        VALUES (?,?, ?, ?, ?)''', (id,username, hashed_password, email, mobile))
            conn.commit()
        except:
            print("User Already Exists")

def login_user(type,id,email, password):
    # Retrieve user data from the database
    if type=="admin":
        c.execute('''SELECT * FROM admin WHERE email = ?''', (email,))
        user = c.fetchone()
        if user:
            # Verify password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user[2] == hashed_password:
                print("Login successful!")
            else:
                print("Invalid password.")
        else:
            print("User not found.")
    elif type=="faculty":
        c.execute('''SELECT * FROM faculty WHERE email = ?''', (email,))
        user = c.fetchone()
        if user:
            # Verify password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user[2] == hashed_password:
                print("Login successful!")
            else:
                print("Invalid password.")
        else:
            print("User not found.")
    elif type=="student":
        c.execute('''SELECT * FROM student WHERE id = ?''', (id,))
        user = c.fetchone()
        if user:
            # Verify password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user[2] == hashed_password:
                print("Login successful!")
            else:
                print("Invalid password.")
        else:
            print("User not found.")
def delete_row_by_id(database_file, table_name, id):
    # Connect to the SQLite database
    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()

        # Execute the DELETE query
        cursor.execute('''DELETE FROM students WHERE id = ?''', (id,))
        
        # Commit the transaction (optional, depending on your requirements)
        conn.commit()
        print('Record Deleted')
def delete_table(database_file, table_name):
    # Connect to the SQLite database
    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()

        # Execute the SQL statement to drop the table
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # Commit the transaction (optional, depending on your requirements)
        conn.commit()

# Example usage
database_file = 'users.db'
table_name = 'student'  # Specify the name of the table to delete

'''delete_table(database_file, table_name)
# Example usage'''
database_file = 'users.db'
table_name = 'students'
id_to_delete = 'y20acs841'  # Specify the ID of the row to delete
import os

def delete_folder_with_name_contains(path, portion):
    # Iterate through all items in the directory
    for item in os.listdir(path):
        # Check if the item is a directory
        if os.path.isdir(os.path.join(path, item)):
            # Check if the portion is in the folder name
            if portion in item:
                # Delete the folder
                folder_path = os.path.join(path, item)
                # Use either os.rmdir() if you're sure the folder is empty or shutil.rmtree() to delete recursively
                # os.rmdir(folder_path)
                import shutil
                shutil.rmtree(folder_path)
                print(f"Deleted folder: {folder_path}")

import pickle

def delete_entries_with_name_contains(pickle_file, portion):
    # Load the pickle file
    with open(pickle_file, 'rb') as f:
        encodings,names= pickle.load(f)
    print(f'Old:--{names}')
    print(f'Old:--{len(encodings)}')
    # Iterate through the names and encodings
    indices_to_remove = []
    for i, name in enumerate(names):
        if portion in name:
            indices_to_remove.append(i)
    print(indices_to_remove)
    # Remove entries from both lists
    for index in sorted(indices_to_remove, reverse=True):
        del names[index]
        del encodings[index]
    
    # Save the modified lists back to the pickle file
    with open(pickle_file, 'wb') as f:
        pickle.dump((encodings, names), f)
    with open(pickle_file, 'rb') as f:
        encodings, names = pickle.load(f)
    print(f"New:--{names}")
    print(f"New:--{len(encodings)}")
import csv

def delete_row_by_id(csv_file, id_value):
    # Read the CSV file and load its contents into a list of dictionaries
    rows = []
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)

    # Find the index of the row with the matching ID value
    index_to_remove = None
    for i, row in enumerate(rows):
        if row['id'] == id_value:  # Assuming 'ID' is the name of the column containing IDs
            index_to_remove = i
            break

    # Remove the row with the matching ID value
    if index_to_remove is not None:
        del rows[index_to_remove]

    # Write the modified data back to the CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = rows[0].keys() if rows else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Example usage
delete_entries_with_name_contains('encodings.pkl','Karthik')



