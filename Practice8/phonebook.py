import psycopg2
from config import *
from connect import *

while True:
    print("""
            1. Create table
            2. Import from CSV
            3. Add contact
            4. Upsert contact
            5. Show all
            6. Search by name
            7. Search by phone
            8. Update contact
            9. Delete contact
            0. Exit
        """)
    choice = input("Choose: ")
    if choice == "1":
        create_table()
    elif choice == "2":
        connect_csv_to_postgres_in_moment("contacts.csv")
    elif choice == "3":
        qcoice=input("one(1) or many(2)?: ")
        if (qcoice=="1"):
            insert_from_console()
        elif (qcoice=="2"):
            bulk_insert()
    elif choice == "4":
        upsert()
    elif choice == "5":
        get_all()
    elif choice == "6":
        name = input("Enter name: ")
        search_by_name(name)
    elif choice == "7":
        phone = input("Enter phone: ")
        search_by_phone_prefix(phone)
    elif choice == "8":
        username = input("Enter username: ")
        update_contact(username)
    elif choice == "9":
        delete_contact()
    elif choice == "0":
        break