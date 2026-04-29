import psycopg2
import csv
from config import DB_CONFIG
import json
import re
from datetime import datetime

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")  # упрощённо

def is_valid_email(email):
    return bool(email and EMAIL_REGEX.match(email))

def is_valid_phone(phone):
    return bool(phone and PHONE_REGEX.match(phone))

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

def connect_csv_to_postgres_in_moment(filename):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    username, phone, email, birthday, group, phone_type = row
                    cur.execute("""
                        INSERT INTO contacts (username, phone, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s, (SELECT id FROM groups WHERE name = %s LIMIT 1))
                        ON CONFLICT (username) DO NOTHING
                    """, (username, phone, email, birthday, group))
                    cur.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES ((SELECT id FROM contacts WHERE username = %s), %s, %s)
                        ON CONFLICT (phone) DO NOTHING
                    """, (username, phone, phone_type))
            connect.commit()
def import_from_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:

            for c in data:
                username = c["username"]

                cur.execute("SELECT id FROM contacts WHERE username=%s", (username,))
                exists = cur.fetchone()

                if exists:
                    choice = input(f"{username} exists (s=skip, o=overwrite): ")

                    if choice == "s":
                        continue

                    cur.execute("DELETE FROM contacts WHERE username=%s", (username,))

                cur.execute("""
                    INSERT INTO contacts(username,email,birthday,group_id)
                    VALUES (%s,%s,%s,
                        (SELECT id FROM groups WHERE name=%s LIMIT 1))
                """, (
                    c["username"],
                    c.get("email"),
                    c.get("birthday"),
                    c.get("group")
                ))

                cur.execute("SELECT id FROM contacts WHERE username=%s", (username,))
                cid = cur.fetchone()[0]

                for p in c.get("phones", []):
                    cur.execute("""
                        INSERT INTO phones(contact_id, phone, type)
                        VALUES (%s,%s,%s)
                    """, (cid, p["phone"], p["type"]))
        connect.commit()

def export_to_json():
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:

            cur.execute("""
                SELECT 
                    c.id,
                    c.username,
                    c.phone,
                    c.email,
                    c.birthday,
                    g.name,
                    COALESCE(
                        json_agg(json_build_object('phone', p.phone, 'type', p.type))
                        FILTER (WHERE p.phone IS NOT NULL),
                        '[]'
                    ) AS phones
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                GROUP BY c.id, g.name
            """)

            data = cur.fetchall()

            result = []
            for row in data:
                result.append({
                    "id": row[0],
                    "username": row[1],
                    "phone": row[2],
                    "email": row[3],
                    "birthday": row[4].isoformat() if row[4] else None,
                    "group": row[5],
                    "phones": row[6]
                })

            with open("contacts.json", "w") as f:
                json.dump(result, f, indent=4)