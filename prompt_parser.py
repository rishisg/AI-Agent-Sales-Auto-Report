import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def parse_prompt(user_input):
    """Generate structured SQL queries dynamically from natural language prompts."""
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.chat.completions.create(
        model="gpt-4-turbo",  # ✅ Switches to GPT-4 Turbo for better accuracy
        messages=[
            {"role": "system", "content": "Convert user requests into valid SQL queries for 'report_db.sales_data'. NO explanations, NO formatting, ONLY raw SQL."},
            {"role": "user", "content": f"Generate an SQL query using the table 'report_db.sales_data' and columns: id, date, product, region, sales, quantity. Request: {user_input}"}
        ]
    )

    sql_query = response.choices[0].message.content.strip()

    # Strip unwanted formatting
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    print(f"Generated SQL Query:\n{sql_query}")  # ✅ Debugging

    return sql_query
