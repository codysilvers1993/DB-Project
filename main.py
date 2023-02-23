import os
import sqlite3
import hashlib


# SHA-256 algorithm password encoder function
def hash_password(password):
    # encode the password as UTF-8
    password_bytes = password.encode('utf-8')

    # hash the salted password using SHA-256
    hash_bytes = hashlib.sha256(password_bytes).digest()
    # convert the hash value and salt to hexadecimal strings
    hash_str = hash_bytes.hex()
    # concatenate the salt and hash strings

    return hash_str


# prompt and get username function
def get_username():
    while True:
        username = input("Enter Your Username: ")
        if username.strip() != '':
            return username
        else:
            print("Username cannot be blank. Please try again.")


# prompt and get password function
def get_password():
    while True:
        password = input("Enter Your Password: ")
        if password.strip() != '':
            return password
        else:
            print("Password cannot be blank. Please try again.")


# insert username and password into database table function.
def insert_username_password_into_table(username, password):
    # create a connection to the database
    conn = sqlite3.connect('user_data.db')
    # create a cursor object to execute SQL commands
    c = conn.cursor()
    # insert the username and password into the table
    c.execute("INSERT INTO userDataCreds VALUES (?, ?)", (username, password))
    # commit the changes to the database
    conn.commit()
    # close the connection
    conn.close()


# create database function
def create_database():
    # check if the database file already exists and if so will print statement
    if os.path.exists('user_data.db'):
        print("Database File Already Exists\n")
        return
    # create a connection to the database
    conn = sqlite3.connect('user_data.db')
    # create a cursor object to execute SQL commands
    c = conn.cursor()
    # create a table to store user credentials
    c.execute('''CREATE TABLE userDataCreds
                    (username TEXT, password TEXT)''')
    # commit the changes to the database
    conn.commit()
    # close the connection
    conn.close()


def create_database_admin():
    # check if the database file already exists and if so will print statement
    if os.path.exists('user_data_admin.db'):
        print("Database File Already Exists\n")
        return
    # create a connection to the database
    conn = sqlite3.connect('user_data_admin.db')
    # create a cursor object to execute SQL commands
    c = conn.cursor()
    # create a table to store user credentials
    c.execute('''CREATE TABLE userDataAdmin 
                     (admin_username TEXT, admin_password TEXT)''')
    # commit the changes to the database
    conn.commit()
    # close the connection
    conn.close()


# print ALL database info function
def print_database_data_rows():
    # create a connection to the database
    conn = sqlite3.connect('user_data.db')
    # create a cursor object to execute SQL commands
    c = conn.cursor()
    # execute a SELECT statement to retrieve all rows from the table
    c.execute("SELECT * FROM userDataCreds")
    # retrieve the results of the SELECT statement using fetchall() method
    rows = c.fetchall()
    # print the rows
    for row in rows:
        print(row)
    # close the connection
    conn.close()


# Register User
def register():
    username = get_username()
    password = get_password()
    hashed_password = hash_password(password)
    insert_username_password_into_table(username, hashed_password)
    print("Registration Successful")


# "login" user and check if hashed password matches user info
def login():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cursor.execute("SELECT password FROM userDataCreds WHERE username = ?", (username,))
    result = cursor.fetchone()
    # Check if the username exists in the user database
    if result is not None:
        # Get the hashed password for this user
        hashed_password = result[0]
        # Hash the user input using the same algorithm and compare
        if hash_password(password) == hashed_password:
            print("Login successful!")
        else:
            print("Invalid password.")
    else:
        print("User not found.")
    # Close the connection
    conn.close()


def delete_data():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    username = input("Enter The Username To Delete: ")
    cursor.execute("DELETE FROM userDataCreds WHERE username = ?", (username,))
    conn.commit()
    conn.close


# general welcome screen
def welcome_screen():
    print("===================================")
    print("|     == Secure Database ==     |")
    print("===================================\n")
    print("Type 1 to register, type 2 to login, or type 3 to delete data\n")
    choice = input("Enter your choice: ")
    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        delete_data()
    else:
        print("Invalid choice.")


if __name__ == '__main__':
    create_database()
    create_database_admin()
    welcome_screen()
    print_database_data_rows()
