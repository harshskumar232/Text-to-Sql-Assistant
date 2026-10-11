# Text-to-SQL Assistant

Ask questions about sales data in plain English and get the answer as a table. An LLM turns the question into SQL and runs it on a local SQLite database. The app shows you the generated query next to the result, so you can check what it actually did.

> "Which region has the highest profit?" → `SELECT region, SUM(profit) ... GROUP BY region ORDER BY ... LIMIT 1` → result table

## How it works

```
Question (English)
   │
   ▼
Prompt = question + `sales` table schema
   │
   ▼
Groq API · llama-3.3-70b-versatile (temperature 0)
   │
   ▼
Generated SQL ──► SQLite (sales.db) via pandas
   │
   ▼
Streamlit UI: SQL query · result table · row count / error message
```

- **`database.py`** loads `superstore.csv` into a SQLite table `sales`. It normalizes the column names to lowercase with underscores, e.g. `Sub-Category` → `sub-category`, `Order Date` → `order_date`.
- **`app.py`** is the Streamlit app. It sends the question and the table schema to the LLM, runs the returned SQL and shows the query, the results and any errors.

## Dataset

The Superstore sales dataset has one table, `sales`, with these columns:

| Group | Columns |
|---|---|
| Order | order ID, order date, ship date, ship mode |
| Customer | customer ID, customer name, segment |
| Location | country, city, state, postal code, region |
| Product | product ID, category, sub-category, product name |
| Metrics | sales, quantity, discount, profit |

## Quick start

```bash
git clone https://github.com/harshskumar232/sql-assistant.git
cd sql-assistant
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install streamlit pandas groq python-dotenv

echo "GROQ_API_KEY=your_key_here" > .env    # free key at console.groq.com
python database.py                          # builds sales.db from superstore.csv
streamlit run app.py                        # opens http://localhost:8501
```

## Example questions

- Which region has the highest profit?
- Top 5 customers by total sales?
- What is the total sales by category?
- Which sub-categories lose money after discounts?

## Tech stack

Python · Streamlit · SQLite · pandas · Groq API (Llama 3.3 70B) · python-dotenv

## Known limitations

This is an early version. These limitations are known and planned to be fixed:

- **The SQL runs without validation.** Only use it on a local copy of the data, never on a production database.
- **There is no retry.** If a query fails, the error is shown to you but not sent back to the model.
- **There is no evaluation set yet.** Accuracy has only been checked by hand on example questions.

## Roadmap

- [ ] Open the database read-only and allow only `SELECT` statements
- [ ] Strip markdown code fences from the model output before running it
- [ ] Self-correction: send SQL errors back to the model and retry once
- [ ] Evaluation set of 20+ questions with expected results; report execution accuracy
- [ ] `requirements.txt`, Dockerfile, and a hosted demo

## Author

**Harsh Kumar**, M.Sc. Data Science, FAU Erlangen-Nürnberg
[GitHub](https://github.com/harshskumar232) · [LinkedIn](https://linkedin.com/in/harshkumar23/)
