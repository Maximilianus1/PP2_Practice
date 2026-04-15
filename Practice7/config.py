import psycopg2
DB_CONFIG = {
    "dbname": "pp",
    "user": "postgres",
    "password": "admin",
    "host":"localhost",
    "port":"5432"
}
def create_table():
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(100) NOT NULL,
                    user_work VARCHAR(200)
                    )""")
            connect.commit()
def insert_from_console():
    username = input("Name: ")
    phone = input("Phone: ")
    user_work = input("Work: ")
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                INSERT INTO contacts (username, phone, user_work)
                VALUES (%s, %s, %s)
                ON CONFLICT (username) DO NOTHING
            """, (username, phone, user_work))
        connect.commit()
def get_all():
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("SELECT * FROM contacts")
            for row in cur.fetchall():
                print(row)
def search_by_name(name):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                SELECT * FROM contacts
                WHERE username ILIKE %s
            """, (f"%{name}%",))
            print(cur.fetchall())
def search_by_phone_prefix(phone):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                SELECT * FROM contacts
                WHERE phone LIKE %s
            """, (f"{phone}%",))
            print(cur.fetchall())
def search_by_user_work(work):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                SELECT * FROM contacts
                WHERE user_work LIKE %s
            """, (f"{work}%",))
def update_contact(username):
    choice = input("Update (1)name, (2)phone or (3)work: ")
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            if choice == "1":
                new_name =input("New name: ")
                cur.execute("""
                    UPDATE contacts
                    SET username = %s
                    WHERE username = %s
                """, (new_name, username))
                print("name updated")
            elif choice=="2":
                new_phone= input("New phone: ")
                cur.execute("""
                    UPDATE contacts
                    SET phone = %s
                    WHERE username = %s
                """, (new_phone, username))
                print("phone updated")
            elif choice=="3":
                new_work= input("New work: ")
                cur.execute("""
                    UPDATE contacts
                    SET user_work = %s
                    WHERE username = %s
                """, (new_work, username))
                print("work updated")
            else:
                print("operation does not exist")
        connect.commit()
def delete_contact():
    choice = input("Delete by (1)name or (2)phone: ")
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            if choice=="1":
                name = input("Enter name: ")
                cur.execute("DELETE FROM contacts WHERE username = %s", (name,))
            else:
                phone = input("Enter phone: ")
                cur.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
        connect.commit()