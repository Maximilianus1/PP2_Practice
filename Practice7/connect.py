import psycopg2
import csv
from config import DB_CONFIG

def connect_csv_to_postgres_in_moment(filename):
    with psycopg2.connect(DB_CONFIG) as connect:
        with connect.cursor() as cur:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    username, phone = row
                    cur.execute(f"""
                        INSERT INTO contacts (username, phone)
                        VALUES ({username}, {phone})
                        ON CONFLICT (username) DO NOTHING
                    """)
            connect.commit()