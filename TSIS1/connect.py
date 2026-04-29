import psycopg2
import csv
from config import DB_CONFIG
import json

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
    with open(filename, 'r') as json_file:
        contacts_data = json.load(json_file)

    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            for contact in contacts_data:
                cur.execute("""
                    INSERT INTO contacts (username, email, birthday, group_id)
                    VALUES (%s, %s, %s, (SELECT id FROM groups WHERE name = %s LIMIT 1))
                    ON CONFLICT (username) DO NOTHING
                """, (contact['username'], contact['email'], contact['birthday'], contact['group']))
                for phone in contact['phones']:
                    cur.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES ((SELECT id FROM contacts WHERE username = %s), %s, %s)
                        ON CONFLICT (phone) DO NOTHING
                    """, (contact['username'], phone['phone'], phone['type']))
            connect.commit()

def export_to_json():
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.username, c.phone, c.email, c.birthday, g.name as group_name, p.phone as phones, p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
            """)
            contacts = cur.fetchall()
            contacts_list = []
            for contact in contacts:
                contact_data = {
                    'id': contact[0],
                    'username': contact[1],
                    'phone': contact[2],
                    'email': contact[3],
                    'birthday': contact[4],
                    'group': contact[5],
                    'phones': [{'phone': contact[6], 'type': contact[7]}]
                }
                contacts_list.append(contact_data)
            with open('contacts.json', 'w') as json_file:
                json.dump(contacts_list, json_file, indent=4)