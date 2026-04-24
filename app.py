import streamlit as st
import sqlite3
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Database connection
def run_query(sql):
    conn = sqlite3.connect("sales.db")
    try:
        df = pd.read_sql_query(sql, conn)
        return df, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()

# Ask Groq to convert question to SQL
def generate_sql(question):
    schema = """
    Table: sales
    Columns: row_id, order_id, order_date, ship_date, ship_mode,
    customer_id, customer_name, segment, country, city, state,
    postal_code, region, product_id, category, sub_category,
    product_name, sales, quantity, discount, profit
    """
    prompt = f"""
    You are an expert SQL assistant. Given this table schema:
    {schema}
    
    Convert this question to a valid SQLite SQL query:
    "{question}"
    
    Rules:
    - Return ONLY the SQL query, nothing else
    - No explanations, no markdown, no backticks
    - Always use lowercase column names
    - Use proper SQLite syntax
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

# ── UI ──────────────────────────────────────────────────────
st.set_page_config(page_title="SQL Assistant", page_icon="🔍", layout="wide")

st.title("🔍 SQL Query Assistant")
st.markdown("Ask any question about the Superstore sales data in plain English.")

# Example questions
st.markdown("**Try asking:**")
cols = st.columns(3)
examples = [
    "Which region has the highest profit?",
    "Top 5 customers by total sales?",
    "What is the total sales by category?",
]
for i, ex in enumerate(examples):
    if cols[i].button(ex):
        st.session_state.question = ex

# Input
question = st.text_input(
    "Your question:",
    value=st.session_state.get("question", ""),
    placeholder="e.g. Which product has the highest sales?"
)

if st.button("Ask", type="primary") and question:
    with st.spinner("Thinking..."):
        sql = generate_sql(question)
        
    st.markdown("**Generated SQL:**")
    st.code(sql, language="sql")
    
    df, error = run_query(sql)
    
    if error:
        st.error(f"Query error: {error}")
    else:
        st.markdown("**Results:**")
        st.dataframe(df, use_container_width=True)
        st.success(f"Found {len(df)} rows")