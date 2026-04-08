import psycopg2
from psycopg2 import extras, pool
import os
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
DB_URL = os.getenv("DATABASE_URL")

# --- CONNECTION POOLING ---
# We use a ThreadedConnectionPool for Flask's multi-threaded environment.
# minconn=1, maxconn=10 (adjust based on Supabase plan limits)
_db_pool = None

def init_pool():
    global _db_pool
    if _db_pool is None:
        try:
            if not DB_URL:
                print("❌ Error: DATABASE_URL not found.")
                return None
            _db_pool = pool.ThreadedConnectionPool(1, 10, DB_URL)
            print("✅ Database connection pool initialized.")
        except Exception as e:
            print(f"❌ Failed to initialize pool: {e}")

def get_connection():
    """
    Pulls a connection from the pool.
    """
    global _db_pool
    if _db_pool is None:
        init_pool()
    
    if _db_pool:
        return _db_pool.getconn()
    return None

def release_connection(conn):
    """
    Returns a connection to the pool.
    """
    global _db_pool
    if _db_pool and conn:
        _db_pool.putconn(conn)

def setup_tables():
    """
    In Supabase, we usually run the SQL script in the dashboard.
    """
    print("✅ Schema expected to be managed via Supabase SQL Editor.")

if __name__ == "__main__":
    # Test connection
    init_pool()
    conn = get_connection()
    if conn:
        print("✅ SUCCESS: Connected to Supabase via Pool!")
        release_connection(conn)