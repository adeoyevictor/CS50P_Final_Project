import argparse
import sqlite3
import sys
from tabulate import tabulate

con = sqlite3.connect("contacts.db")
cur = con.cursor()

def main():
    parser = argparse.ArgumentParser(description="Implement a Contact Book")
    parser.add_argument("-u", help="Your Username")
    args = parser.parse_args()
    username =  args.u
    usernames = cur.execute("SELECT username FROM users").fetchall()
    username_list = create_users_list(usernames)
    if check_username(username_list, username):
        get_action(username)
    else:
        cur.execute("INSERT INTO users (username) VALUES (?)", (username,))
        con.commit()
        print(f"New user '{username}' added")
        get_action(username)
        
def create_users_list(usernames):
    username_list = []
    for i in range(len(usernames)):
        username_list.append(usernames[i][0])
    return username_list

def check_username(username_list, username):
    return username in username_list

def get_action(username):
    actions = ["add", "delete", "list", "update"]
    action = input(f"Choose an action from: {', '.join(actions)}\nAction: ")
    user_id = cur.execute("SELECT id FROM users WHERE username =?", [username]).fetchone()
    user_id= user_id[0]

    if action == "add":
        add_contact(user_id)
    elif action == "delete":
        delete_contact(user_id)
    elif action == "list":
        list_contact(user_id)
    elif action == "update":
        update_contact(user_id)
    else:
        sys.exit(f"Invalid action, Choose an action from: {', '.join(actions)}")

def add_contact(user_id):
    name, phone, email = get_contact()
    if not email or not name or not phone:
        sys.exit("Please provide name, phone number and, email address")
    else:
        cur.execute("INSERT INTO contacts(user_id, name, phone, email) VALUES(?, ?, ?, ?)", (user_id, name, phone, email))
        con.commit()
        print("Contacted added successfully")

def get_contact():
    name = input("Name: ") 
    phone = input("Phone Number: ") 
    email = input("Email Address: ")
    return name, phone, email

def delete_contact(user_id):
    name = input("Name: ")
    contacts = cur.execute("SELECT name FROM contacts WHERE name = ? AND user_id = ?", (name, user_id)).fetchall()
    if check_contacts(contacts):
        sys.exit("NO such user exists in your contacts list")
    else:
        cur.execute("DELETE FROM contacts WHERE name = ? AND user_id = ?", (name, user_id))
        con.commit()
        print("Contact deleted successfully")

def list_contact(user_id):
    contacts = cur.execute("SELECT name, phone, email FROM contacts WHERE user_id = ?", (user_id, )).fetchall()
    if check_contacts(contacts):
        print("You have no contacts in your list")
    else:
        print()
        print(tabulate(contacts, headers=["Name", "Phone Number", "Email Address"]))
        print()

def update_contact(user_id):
    name = input("Name: ")
    contacts = cur.execute("SELECT name FROM contacts WHERE name = ? AND user_id = ?", (name, user_id)).fetchall()
    if check_contacts(contacts):
        sys.exit("NO such user exists in your contacts list")
    else:
        phone = input("Phone Number: ") 
        email = input("Email Address: ")
        if not email or not phone:
            sys.exit("Please provide phone number and, email address")
        else:
            cur.execute("UPDATE contacts SET phone = ?, email = ? WHERE name = ? AND user_id =?", (phone, email, name, user_id))
            con.commit()
            print("Contact updated successfully")

def check_contacts(contacts):
    return len(contacts) == 0

if __name__ == '__main__':
    main()