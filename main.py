import os
import sqlite3
import hashlib

# SHA-256 algorithm password encoder function
def hash_password(password):
    # encode the password as UTF-8
    password_bytes = password.encode('utf-8')
    # hash the password using SHA-256
    hash_bytes = hashlib.sha256(password_bytes)
    # convert the hash value to a hexadecimal string
    hash_str = hash_bytes.hexdigest()
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
        print("Database file already exists")
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


if __name__ == '__main__':
    # returns strings from get_username and get_password
    username = get_username()
    password = get_password()
    # passes password through hasher to return hashed password
    password = hash_password(password)

    # function to initialize database and insert password and username into rows with columns named, username/password
    create_database()
    insert_username_password_into_table(username, password)
    # prints database info for testing
    print_database_data_rows()
