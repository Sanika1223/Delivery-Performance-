
import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "delivery_performance",
    "user": "postgres",
    "password": "Sanika@123",
    "port": 5432
}


def get_db_connection():
    connection = psycopg2.connect(**DB_CONFIG)
    return connection
