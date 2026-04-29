import psycopg2
from config import *
from connect import *

while True:
    print("""
            1. Create table
            2. Import from CSV
            3. Import from JSON
            4. Export to JSON
            5. Add contact
            6. Upsert contact
            7. Show all
            8. Search by name
            9. Search by phone
            10. Search by email
            11. Filter by group
            12. Sort contacts
            13. Paginated navigation
            14. Update contact
            15. Delete contact
            0. Exit
        """)
    choice = input("Choose: ")
    if choice == "1":
        create_table()
    elif choice == "2":
        connect_csv_to_postgres_in_moment("contacts.csv")
    elif choice == "3":
        filename = input("Enter the JSON filename to import (e.g., contacts.json): ")
        import_from_json(filename)
    elif choice == "4":
        export_to_json()
    elif choice == "5":
        qcoice = input("one(1) or many(2)?: ")
        if qcoice == "1":
            insert_from_console()
        elif qcoice == "2":
            bulk_insert()
    elif choice == "6":
        upsert()
    elif choice == "7":
        get_all()
    elif choice == "8":
        name = input("Enter name: ")
        search_by_name(name)
    elif choice == "9":
        phone = input("Enter phone: ")
        search_by_phone_prefix(phone)
    elif choice == "10":
        email = input("Enter email: ")
        search_by_email(email)
    elif choice == "11":
        group_name = input("Enter group name: ")
        filter_by_group(group_name)
    elif choice == "12":
        sort_by = input("Sort by (name/birthday): ").strip().lower()
        if sort_by in ['name', 'birthday']:
            sort_results(sort_by)
        else:
            print("Invalid sort option. Please choose 'name' or 'birthday'.")
    elif choice == "13":
        limit = int(input("Enter limit for pagination: "))
        offset = int(input("Enter offset for pagination: "))
        paginated_navigation(limit, offset)
    elif choice == "14":
        username = input("Enter username: ")
        update_contact(username)
    elif choice == "15":
        delete_contact()
    elif choice == "0":
        break