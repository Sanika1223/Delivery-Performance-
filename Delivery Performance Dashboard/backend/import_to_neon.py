
import csv
from pathlib import Path

from psycopg2.extras import execute_values
from database import get_db_connection


# Locate the cleaned CSV file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_ROOT / "Data" / "Cleaned" / "delivery_data_stage2.csv"

# These columns match the Neon table
COLUMNS = [
    "delivery_record_id",
    "delivery_id_original",
    "delivery_partner",
    "package_type",
    "vehicle_type",
    "delivery_mode",
    "region",
    "weather_condition",
    "distance_km",
    "package_weight_kg",
    "delivery_rating",
    "delivery_cost",
    "delayed",
    "delivery_status",
    "delivery_time_hours",
    "expected_time_hours",
    "delivery_time_hours_original",
    "expected_time_hours_original",
    "time_data_quality",
]


def main():
    if not CSV_FILE.exists():
        print(f"CSV file not found: {CSV_FILE}")
        return

    records = []

    with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            record = []

            for column in COLUMNS:
                value = row.get(column)

                if value is not None:
                    value = value.strip()

                record.append(value if value else None)

            records.append(tuple(record))

    if not records:
        print("No records found in the CSV.")
        return

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            insert_query = f"""
                INSERT INTO delivery_analysis ({", ".join(COLUMNS)})
                VALUES %s
                ON CONFLICT (delivery_record_id) DO NOTHING
            """

            execute_values(
                cursor,
                insert_query,
                records,
                page_size=1000
            )

        connection.commit()

        print(f"CSV records processed: {len(records)}")
        print("Data upload completed successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
