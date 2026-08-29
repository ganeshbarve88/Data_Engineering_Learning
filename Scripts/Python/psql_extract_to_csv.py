import psycopg2
import csv
import os
from dotenv import load_dotenv

# 1. Load environment variables from the local .env file
load_dotenv()

# 2. Configuration - Securely reading from the environment with fallbacks
DB_CONFIG = {
    "dbname": os.environ.get("DB_NAME", "pagila_db"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT", "5432")
}

def get_all_tables(cursor):
    """Queries the database catalog to dynamically find all user tables."""
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    return [row[0] for row in cursor.fetchall()]

def extract_all_to_csv():
    # Defensive check: Ensure critical credentials were loaded from the .env file
    if not DB_CONFIG["user"] or not DB_CONFIG["password"]:
        print("❌ Error: DB_USER or DB_PASSWORD environment variables are missing!")
        print("Please check that your .env file exists and contains these variables.")
        return

    # 3. Handle Absolute Paths to ensure files drop into the dbt project folder
    # Find the folder where this specific script file lives
    BASE_DIR = "C:\\Users\\ganes\\Documents\\GitHub\\Data_Engineering_Learning"
    
    # Target the seeds folder inside your specific dbt project directory
    target_seeds_dir = os.path.join(BASE_DIR, 'my_bigquery_project', 'seeds')
    
    # Automatically create the destination directory if it doesn't exist
    if not os.path.exists(target_seeds_dir):
        os.makedirs(target_seeds_dir)
        print(f"📁 Created missing target directory: {target_seeds_dir}")

    try:
        print("🔌 Connecting to PostgreSQL securely using environment variables...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # 4. Discover tables dynamically
        tables = get_all_tables(cur)
        print(f"🔍 Successfully discovered {len(tables)} tables to extract.")

        # 5. Extract each discovered table
        for table in tables:
            print(f"📥 Extracting table: {table}...")
            cur.execute(f"SELECT * FROM {table}")
            
            # Dynamically grab the column headers from the cursor metadata
            column_names = [desc[0] for desc in cur.description]
            
            # Construct the absolute path for the output CSV file
            output_file = os.path.join(target_seeds_dir, f"{table}.csv")
            
            # Using context manager 'with' to ensure clean file writing
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(column_names)  # Write headers
                writer.writerows(cur.fetchall())  # Write all data rows
            
        cur.close()
        conn.close()
        print("\n🎉 Extraction complete! All tables saved to 'my_bigquery_project/seeds/' folder.")

    except Exception as e:
        print(f"❌ Extraction failed with error: {e}")

if __name__ == "__main__":
    extract_all_to_csv()