import os
import time

import psycopg

db_name = os.environ.get("POSTGRES_DB")
db_user = os.environ.get("POSTGRES_USER")
db_password = os.environ.get("POSTGRES_PASSWORD")
db_host = os.environ.get("POSTGRES_HOST", "db")
db_port = os.environ.get("POSTGRES_PORT", "5432")

conninfo = (
    f"dbname={db_name} "
    f"user={db_user} "
    f"password={db_password} "
    f"host={db_host} "
    f"port={db_port}"
)

while True:
    try:
        with psycopg.connect(conninfo, connect_timeout=3) as conn:
            print("✅ Database is ready!")
            break
    except psycopg.OperationalError as exc:
        print("⏳ Waiting for database...")
        print(exc)
        time.sleep(2)