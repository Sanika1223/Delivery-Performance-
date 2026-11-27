
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_db_connection

app = FastAPI(title="Delivery Performance Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Delivery Performance API is running"}


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/db-test")
def database_test():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT current_database();")
        database_name = cursor.fetchone()[0]

        cursor.close()

        return {
            "status": "connected",
            "database": database_name
        }

    finally:
        connection.close()


@app.get("/api/regional-performance")
def regional_performance(region: str = "All"):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        if region.lower() == "all":
            cursor.execute("""
                SELECT
                    region,
                    COUNT(*) AS total_deliveries
                FROM delivery_analysis
                GROUP BY region
                ORDER BY total_deliveries DESC;
            """)
        else:
            cursor.execute("""
                SELECT
                    region,
                    COUNT(*) AS total_deliveries
                FROM delivery_analysis
                WHERE LOWER(region) = LOWER(%s)
                GROUP BY region
                ORDER BY total_deliveries DESC;
            """, (region,))

        results = cursor.fetchall()

        return [
            {
                "region": row[0],
                "total_deliveries": row[1]
            }
            for row in results
        ]

    finally:
        connection.close()


@app.get("/api/delivery-status")
def delivery_status(region: str = "All"):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        if region.lower() == "all":
            cursor.execute("""
                SELECT delivery_status, COUNT(*) AS total
                FROM delivery_analysis
                GROUP BY delivery_status
                ORDER BY total DESC;
            """)
        else:
            cursor.execute("""
                SELECT delivery_status, COUNT(*) AS total
                FROM delivery_analysis
                WHERE LOWER(region) = LOWER(%s)
                GROUP BY delivery_status
                ORDER BY total DESC;
            """, (region,))

        results = cursor.fetchall()

        return [
            {
                "name": row[0].capitalize(),
                "value": row[1]
            }
            for row in results
        ]

    finally:
        connection.close()


@app.get("/api/table-columns")
def table_columns():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'delivery_analysis'
            ORDER BY ordinal_position;
        """)

        results = cursor.fetchall()

        return [row[0] for row in results]

    finally:
        connection.close()


@app.get("/api/total-deliveries")
def total_deliveries(region: str = "All"):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        if region.lower() == "all":
            cursor.execute("""
                SELECT COUNT(*)
                FROM delivery_analysis;
            """)
        else:
            cursor.execute("""
                SELECT COUNT(*)
                FROM delivery_analysis
                WHERE LOWER(region) = LOWER(%s);
            """, (region,))

        result = cursor.fetchone()

        return {"total_deliveries": result[0]}

    finally:
        connection.close()


@app.get("/api/regions")
def get_regions():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT DISTINCT region
            FROM delivery_analysis
            ORDER BY region;
        """)

        results = cursor.fetchall()

        return [row[0] for row in results]

    finally:
        connection.close()
