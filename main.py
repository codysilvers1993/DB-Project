import os
import sqlite3
import hashlib
import sys
import time


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


# ===========================Getter Functions==================================

def get_username():
    while True:
        username = input("Enter Your Username: ")
        if username.strip() != '':
            return username
        else:
            print("Username cannot be blank. Please try again.")


def get_password():
    while True:
        password = input("Enter Your Password: ")
        if password.strip() != '':
            return password
        else:
            print("Password cannot be blank. Please try again.")


# ===========================================================================

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


# ===========================Create Regular User/Admin Necessary Database Functions===================
def create_database():
    # check if the database file already exists and if so will print statement
    if os.path.exists('user_data.db'):
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
        return
    # create a connection to the database
    conn = sqlite3.connect('user_data_admin.db')
    # create a cursor object to execute SQL command
    c = conn.cursor()
    # create a table to store user credentials
    c.execute('''CREATE TABLE userDataAdmin 
                     (admin_username TEXT, admin_password TEXT)''')
    # commit the changes to the database
    conn.commit()
    # close the connection
    conn.close()


# ========================================================================================

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
    conn.commit
    conn.close()


# Register Use
def register():
    username = get_username()
    password = get_password()
    hashed_password = hash_password(password)
    insert_username_password_into_table(username, hashed_password)
    print("Registration Successful")
    while True:
        choice = input("Do you want to go back to main screen? (y/n): ")
        if choice == "y":
            welcome_screen()
            break
        elif choice == "n":
            print("Database Closed")
            sys.exit()  # exit the program
        else:
            print("\nInvalid entry. Please enter 'y' or 'n'.")
            while True:
                choice = input("Do you want to go back to main screen? (y/n): ")
                if choice == "y":
                    welcome_screen()
                    break
                elif choice == "n":
                    print("Database Closed")
                    sys.exit()  # exit the program
                else:
                    print("Invalid entry. Please enter 'y' or 'n'.")


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
            while True:
                choice = input("Do you want to go back to main screen? (y/n): ")
                if choice == "y":
                    welcome_screen()
                    break
                elif choice == "n":
                    print("Database Closed")
                    sys.exit()  # exit the program
                else:
                    print("Invalid entry. Please enter 'y' or 'n'.")
        else:
            print("Invalid password.")
            while True:
                choice = input("Do you want to go back to main screen? (y/n): ")
                if choice == "y":
                    welcome_screen()
                    break
                elif choice == "n":
                    print("Database Closed")
                    sys.exit()  # exit the program
                else:
                    print("Invalid entry. Please enter 'y' or 'n'.")
    else:
        print("User not found.")
        while True:
            choice = input("Do you want to go back to main screen? (y/n): ")
            if choice == "y":
                welcome_screen()
                break
            elif choice == "n":
                print("Database Closed")
                sys.exit()  # exit the program
            else:
                print("Invalid entry. Please enter 'y' or 'n'.")
    # Close the connection
    conn.close()


def insert_data():
    conn = sqlite3.connect('user_data_admin.db')
    cursor = conn.cursor()

    admin_username = input("Enter Your Admin Username: ")
    admin_password = input("Enter Your Admin Password: ")

    cursor.execute("SELECT admin_password FROM userDataAdmin WHERE admin_username = ?", (admin_username,))
    admin = cursor.fetchone()

    if admin:
        if admin_password == admin[0]:
            conn2 = sqlite3.connect("user_data.db")
            cursor2 = conn2.cursor()
            print_database_data_rows()

            # prompt admin to enter user details
            username = input("Enter username of User You Want To Insert: ")
            password = input("Enter user password: ")

            # insert user details into the database
            cursor2.execute("INSERT INTO userDataCreds (username, password) VALUES (?, ?)",
                            (username, password))
            print("User inserted successfully.")
            conn2.commit()
            conn2.close()

        else:
            print("Incorrect admin password. Please try again.")

    else:
        print("Admin not found. Please try again.")

    conn.commit()
    conn.close()


def delete_data():
    conn = sqlite3.connect('user_data_admin.db')
    cursor = conn.cursor()

    admin_username = input("Enter Your Admin Username: ")
    admin_password = input("Enter Your Admin Password: ")

    cursor.execute("SELECT admin_password FROM userDataAdmin WHERE admin_username = ?", (admin_username,))
    admin = cursor.fetchone()

    if admin:
        if admin_password == admin[0]:
            conn2 = sqlite3.connect("user_data.db")
            cursor2 = conn2.cursor()
            print_database_data_rows()

            user_id_to_delete = input("Enter username of User You Want To Delete: ")
            cursor2.execute("DELETE FROM userDataCreds WHERE username = ?", (user_id_to_delete,))

            print("Username Deleted or Username Doesnt Exist")
            conn2.commit()
            conn2.close()
            while True:
                choice = input("Do you want to go back to main screen? (y/n): ")
                if choice == "y":
                    welcome_screen()
                    break
                elif choice == "n":
                    print("Database Closed")
                    sys.exit()  # exit the program
                else:
                    print("Invalid entry. Please enter 'y' or 'n'.")

        else:
            print("Incorrect admin password. Please try again.")
            while True:
                choice = input("Do you want to go back to main screen? (y/n): ")
                if choice == "y":
                    welcome_screen()
                    break
                elif choice == "n":
                    print("Database Closed")
                    sys.exit()  # exit the program
                else:
                    print("Invalid entry. Please enter 'y' or 'n'.")
    else:
        print("Admin not found. Please try again.")
    conn.commit()
    conn.close()
    while True:
        choice = input("Do you want to go back to main screen? (y/n): ")
        if choice == "y":
            welcome_screen()
            break
        elif choice == "n":
            print("Database Closed")
            sys.exit()  # exit the program
        else:
            print("Invalid entry. Please enter 'y' or 'n'.")


def verify_admin_for_displaying_data():
    conn = sqlite3.connect('user_data_admin.db')
    cursor = conn.cursor()

    admin_username = input("Enter Your Admin Username: ")
    admin_password = input("Enter Your Admin Password: ")

    cursor.execute("SELECT admin_password FROM userDataAdmin WHERE admin_username = ?", (admin_username,))
    admin = cursor.fetchone()

    if admin:
        if admin_password == admin[0]:
            conn2 = sqlite3.connect("user_data.db")
            cursor2 = conn2.cursor()
            print_database_data_rows()
            conn.commit()
            conn.close()
            while True:
                choice = input("Do you want to go back to main screen? (y/n): ")
                if choice == "y":
                    welcome_screen()
                    break
                elif choice == "n":
                    print("Database Closed")
                    sys.exit()  # exit the program
                else:
                    print("Invalid entry. Please enter 'y' or 'n'.")
        else:
            print("Incorrect admin password. Please try again.")
            conn.commit()
            conn.close()
            while True:
                choice = input("Do you want to go back to main screen? (y/n): ")
                if choice == "y":
                    welcome_screen()
                    break
                elif choice == "n":
                    print("Database Closed")
                    sys.exit()  # exit the program
                else:
                    print("Invalid entry. Please enter 'y' or 'n'.")
    else:
        print("Admin not found. Please try again.")
        conn.commit()
        conn.close()
        while True:
            choice = input("Do you want to go back to main screen? (y/n): ")
            if choice == "y":
                welcome_screen()
                break
            elif choice == "n":
                print("Database Closed")
                sys.exit()  # exit the program
            else:
                print("Invalid entry. Please enter 'y' or 'n'.")


def clear_console():
    print(" :: Booting System ::")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(1)
    print(":: Getting The Database Elves Ready...... ::")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(":: System Booted   ::")
    time.sleep(1)



# general welcome screen
def welcome_screen():
    clear_console()
    print("                            ====================================")
    print("                            | == Long-Neck Customer Database == |")
    print("                            ====================================\n")
    print("""\
                                           ._ o o
                                           \_`-)|_
                                        ,""       \ 
                                      ,"  ## |   ಠ ಠ. 
                                    ," ##   ,-\__    `.
                                  ,"       /     `--._;)
                                ,"     ## /
                              ,"   ##    /
                        """)

    print("=== Welcome to Our Award-Winning Secure Database For Hosting User Information === \n"
          "\nPlease Select Any Option [1-5]\n")
    print("Type 1 to register user\nType 2 to login user\nType 3 "
          "to delete user data\nType 4 to insert user data\nType 5 print user information")

    choice = input("\nEnter Your Choice: ")
    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        delete_data()
    elif choice == "4":
        insert_data()
    elif choice == "5":
        verify_admin_for_displaying_data()
        while True:
            choice = input("Do you want to go back to main screen? (y/n): ")
            if choice == "y":
                welcome_screen()
                break
            elif choice == "n":
                print("Database Closed")
                sys.exit()  # exit the program
            else:
                print("Invalid entry. Please enter 'y' or 'n'.")
    else:
        print("Invalid choice.")


if __name__ == '__main__':
    create_database()
    create_database_admin()
    welcome_screen()
