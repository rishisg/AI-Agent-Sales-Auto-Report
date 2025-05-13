import pymysql
import pandas as pd
import os
from dotenv import load_dotenv
from prompt_parser import parse_prompt

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        self.conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True  # ✅ Ensures queries execute instantly
        )

    def generate_report(self, user_prompt, source, uploaded_file=None):
        """Executes AI-generated SQL query and forces refresh."""
        query = parse_prompt(user_prompt)  # ✅ Dynamically generate SQL

        print(f"Executing SQL Query:\n{query}")  # ✅ Debugging

        with self.conn.cursor() as cursor:
            cursor.execute(f"USE {os.getenv('DB_NAME')}")  # ✅ Ensure correct database selection
            try:
                cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;")  # ✅ Ensure latest data
                cursor.execute(query)
                df = pd.DataFrame(cursor.fetchall())  # Convert result to DataFrame
                return df if not df.empty else None
            except pymysql.MySQLError as e:
                print(f"❌ SQL Execution Error: {e}")
                return None
