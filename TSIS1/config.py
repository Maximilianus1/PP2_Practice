import psycopg2
from datetime import datetime

DB_CONFIG = {
    "dbname": "pp",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}


def create_table():
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL
                );

                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(100),
                    user_work VARCHAR(200),
                    email VARCHAR(100),
                    birthday DATE,
                    group_id INTEGER REFERENCES groups(id)
                );

                CREATE TABLE IF NOT EXISTS phones (
                    id SERIAL PRIMARY KEY,
                    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
                    phone VARCHAR(20) UNIQUE,
                    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
                );
            """)
        connect.commit()


def insert_from_console():
    username = input("Username: ")
    phone = input("Main phone: ")
    email = input("Email: ")

    birthday = datetime.strptime(
        input("Birthday (DD-MM-YYYY): "),
        "%d-%m-%Y"
    ).date()

    work = input("Work: ")
    group = input("Group name: ")

    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:

            # insert contact
            cur.execute("""
                INSERT INTO contacts (username, email, birthday, user_work, group_id)
                VALUES (%s, %s, %s, %s,
                        (SELECT id FROM groups WHERE name = %s LIMIT 1))
                ON CONFLICT (username) DO NOTHING
            """, (username, email, birthday, work, group))

            # get id safely
            cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
            res = cur.fetchone()

            if res:
                contact_id = res[0]

                cur.execute("""
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, 'mobile')
                    ON CONFLICT (phone) DO NOTHING
                """, (contact_id, phone))

        connect.commit()

    print("Contact added")


def add_extra_phone():
    username = input("Username: ")
    phone = input("Phone: ")
    phone_type = input("Type (home/work/mobile): ")

    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute(
                "CALL add_phone(%s, %s, %s)",
                (username, phone, phone_type)
            )
        connect.commit()

    print("Phone added")




def create_group():
    name = input("Group name: ")

    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                INSERT INTO groups (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
            """, (name,))
        connect.commit()

    print("Group created")



def get_all():
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("SELECT * FROM contacts")
            print(cur.fetchall())


def search_by_name(name):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                SELECT * FROM contacts
                WHERE username ILIKE %s
            """, (f"%{name}%",))
            print(cur.fetchall())


def search_by_email(email):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                SELECT * FROM contacts
                WHERE email ILIKE %s
            """, (f"%{email}%",))
            print(cur.fetchall())

def search(pattern):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
            print(cur.fetchall())
def search_all(query):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            print(cur.fetchall())

def search_by_phone_prefix(phone):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                SELECT c.*
                FROM contacts c
                LEFT JOIN phones p ON c.id = p.contact_id
                WHERE c.phone LIKE %s OR p.phone LIKE %s
            """, (f"{phone}%", f"{phone}%"))
            print(cur.fetchall())

def update_contact(username):
    print("""
        What do you want to update?
        1 - username
        2 - phone (main in contacts)
        3 - work
        4 - email
        5 - birthday
        6 - group
        """)
    choice = input("Choose: ")
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            if choice == "1":
                new_value = input("New username: ")
                cur.execute("""
                                UPDATE contacts
                                SET username = %s
                                WHERE username = %s
                                """, (new_value, username))
            elif choice == "2":
                new_value = input("New phone: ")
                cur.execute("""
                                UPDATE contacts
                                SET phone = %s
                                WHERE username = %s
                                """, (new_value, username))
            elif choice == "3":
                new_value = input("New work: ")
                cur.execute("""
                                UPDATE contacts
                                SET user_work = %s
                                WHERE username = %s
                                """, (new_value, username))
            elif choice == "4":
                new_value = input("New email: ")
                cur.execute("""
                                UPDATE contacts
                                SET email = %s
                                WHERE username = %s
                                """, (new_value, username))
            elif choice == "5":
                new_value = datetime.strptime(
                    input("New birthday (DD-MM-YYYY): "),
                        "%d-%m-%Y"
                    ).date()

                cur.execute("""
                            UPDATE contacts
                                SET birthday = %s
                                WHERE username = %s
                                """, (new_value, username))
            elif choice == "6":
                new_value = input("New group name: ")
                cur.execute("""
                                UPDATE contacts
                                SET group_id = (SELECT id FROM groups WHERE name = %s LIMIT 1)
                                WHERE username = %s
                                """, (new_value, username))
            else:
                print("Invalid option")
                return

            connect.commit()

        print("Contact updated")

def move_to_group():
    username = input("Username: ")
    group = input("Group name: ")

    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute(
                "CALL move_to_group(%s, %s)",
                (username, group)
            )
        connect.commit()

    print("Moved to group")

def upsert():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        connect.commit()

    print("Upsert done")

def bulk_insert():
    names = input("Names: ").split()
    phones = input("Phones: ").split()

    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute(
                "CALL insert_many_contacts(%s, %s)",
                (names, phones)
            )
        connect.commit()

    print("Bulk insert done")

def delete_contact():
    value = input("Enter name or phone: ")

    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("CALL delete_contact(%s)", (value,))
        connect.commit()

    print("Deleted")



def sort_results(sort_by='username'):
    allowed = ['username', 'birthday', 'id']

    if sort_by not in allowed:
        print("Invalid sort field")
        return

    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM contacts
                ORDER BY {sort_by}
            """)
            print(cur.fetchall())

def paginated_navigation():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    while True:
        with psycopg2.connect(**DB_CONFIG) as connect:
            with connect.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
                rows = cur.fetchall()
                for r in rows:
                    print(r)

        choice = input("n-next, p-prev, q-quit: ")

        if choice == "n":
            offset += limit
        elif choice == "p":
            offset = max(0, offset - limit)
        elif choice == "q":
            break
def filter_by_group(group_name):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                SELECT * FROM contacts
                JOIN groups ON contacts.group_id = groups.id
                WHERE groups.name = %s
            """, (group_name,))
            print(cur.fetchall())