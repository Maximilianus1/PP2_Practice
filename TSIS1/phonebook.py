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
            8. Search (name/email/phone)
            9. Filter by group
            10. Sort contacts
            11. Paginated navigation
            12. Update contact
            13. Delete contact
            14. Create group
            15. Add extra phone
            16. Advanced search (ALL fields)
            0. Exit
        """)

    choice = input("Choose: ")
    if choice == "1":
        create_table()
    elif choice == "2":
        connect_csv_to_postgres_in_moment("contacts.csv")
    elif choice == "3":
        filename = input("JSON filename: ")
        import_from_json(filename)

    elif choice == "4":
        export_to_json()

    elif choice == "5":
        mode = input("1-single / 2-many: ")
        if mode == "1":
            insert_from_console()
        else:
            bulk_insert()
    elif choice == "6":
        upsert()
    elif choice == "7":
        get_all()
    elif choice == "8":
        print("""
        1 - name
        2 - email
        3 - phone prefix
        """)
        t = input("type: ")

        if t == "1":
            search_by_name(input("name: "))
        elif t == "2":
            search_by_email(input("email: "))
        elif t == "3":
            search_by_phone_prefix(input("phone: "))
    elif choice == "9":
        filter_by_group(input("group name: "))

    elif choice == "10":
        sort_by = input("username / birthday: ").strip().lower()
        if sort_by in ["username", "birthday"]:
            sort_results(sort_by)
        else:
            print("Invalid sort option")
    elif choice == "11":
        limit = int(input("limit: "))
        offset = int(input("offset: "))
        paginated_navigation()
    elif choice == "12":
        update_contact(input("username: "))
    elif choice == "13":
        delete_contact()
    elif choice == "14":
        create_group()
    elif choice == "15":
        add_extra_phone()
    elif choice == "16":
        q = input("search query: ")
        search_all(q)
    elif choice == "0":
        break

    else:
        print("Invalid choice")