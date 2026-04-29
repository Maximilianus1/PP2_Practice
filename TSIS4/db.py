import psycopg2
from config import DB_CONFIG

def init_db():
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:

            cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            )
            """)
def get_or_create_player(username):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:

            cur.execute(
                "SELECT id FROM players WHERE username=%s",
                (username,)
            )

            row = cur.fetchone()

            if row:
                return row[0]

            cur.execute(
                "INSERT INTO players(username) VALUES(%s) RETURNING id",
                (username,)
            )

            return cur.fetchone()[0]


def save_result(username, score, level):
    player_id = get_or_create_player(username)

    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:

            cur.execute("""
                INSERT INTO game_sessions(player_id, score, level_reached)
                VALUES(%s,%s,%s)
            """, (player_id, score, level))


def get_top10():
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:

            cur.execute("""
                SELECT username, score, level_reached, played_at
                FROM game_sessions
                JOIN players ON players.id = game_sessions.player_id
                ORDER BY score DESC
                LIMIT 10
            """)

            return cur.fetchall()


def get_best(username):
    with psycopg2.connect(**DB_CONFIG) as connect:
        with connect.cursor() as cur:

            cur.execute("""
                SELECT MAX(score)
                FROM game_sessions
                JOIN players ON players.id = game_sessions.player_id
                WHERE username=%s
            """, (username,))

            res = cur.fetchone()[0]
            return res if res else 0