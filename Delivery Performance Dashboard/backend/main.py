
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
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT current_database();")
        database_name = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return {
            "status": "connected",
            "database": database_name
        }

    except Exception as error:
        return {
            "status": "error",
            "message": str(error)
        }


@app.get("/api/regional-performance")
def regional_performance():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                region,
                COUNT(*) AS total_deliveries
            FROM delivery_analysis
            GROUP BY region
            ORDER BY total_deliveries DESC;
        """)

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
def delivery_status():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT delivery_status, COUNT(*) AS total
            FROM delivery_analysis
            GROUP BY delivery_status
            ORDER BY total DESC;
        """)

        results = cursor.fetchall()

        return [
            {"name": row[0].capitalize(), "value": row[1]}
            for row in results
        ]

    except Exception as error:
        return {"error": str(error)}

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