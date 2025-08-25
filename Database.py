import os
import psycopg2

# Fetch secrets from environment variables
db_host = os.getenv("host")
print("DB HOST ",db_host)
db_port = os.getenv("port")  # Default PostgreSQL port
db_name = os.getenv("database")
db_user = os.getenv("user")
db_password = os.getenv("password")

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    print("✅ Connected to PostgreSQL successfully!")

    # Example query
    with conn.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("PostgreSQL version:", version)

    conn.close()

except Exception as e:
    print("❌ Failed to connect to PostgreSQL:", e)
