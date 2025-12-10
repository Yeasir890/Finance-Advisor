from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import pandas as pd
import os

# basic flask setup
app = Flask(__name__)
app.secret_key = os.environ.get("APP_KEY", "test_key_123")  # simple dev key

# Database setup
def init_db():
    try:
        conn = sqlite3.connect("finance.db")
        c = conn.cursor()

        # transactions table
        c.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # goals table
        c.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL DEFAULT 0,
                deadline TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
    except Exception as e:
        print("DB init error:", e)
    finally:
        conn.close()

# Dummy AI class
class FinancialAI:
    def get_insights(self, df):
        return {"note": "Insights will appear here when enough data exists."}

    def predict_future_spending(self, df):
        return {"next_month": "Prediction module not fully implemented yet."}

    def get_category_breakdown(self, df):
        try:
            g = df.groupby("category")["amount"].sum()
            return g.to_dict()
        except:
            return {}

ai_model = FinancialAI()

# Main pages
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("finance.db")

    # last few items
    trans = pd.read_sql(
        "SELECT * FROM transactions ORDER BY date DESC LIMIT 10", conn
    )

    # Direct calculation for totals - NEW CODE
    try:
        income_df = pd.read_sql(
            "SELECT COALESCE(SUM(amount), 0) as total FROM transactions WHERE type = 'income'",
            conn
        )
        expense_df = pd.read_sql(
            "SELECT COALESCE(SUM(amount), 0) as total FROM transactions WHERE type = 'expense'",
            conn
        )

        total_income = float(income_df['total'].iloc[0])
        total_expense = float(expense_df['total'].iloc[0])
        balance = total_income - total_expense

    except Exception as e:
        print("Calculation error:", e)
        total_income = 0
        total_expense = 0
        balance = 0

    conn.close()

    return render_template(
        "dashboard.html",
        transactions=trans.to_dict("records"),
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,

    )

# Add transaction
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        t_date = request.form.get("date")
        t_amount = request.form.get("amount")
        t_cat = request.form.get("category")
        t_type = request.form.get("type")
        t_desc = request.form.get("description")

        try:
            amt = float(t_amount)
        except:
            flash("Invalid amount!", "danger")
            return redirect(url_for("add_transaction"))

        try:
            conn = sqlite3.connect("finance.db")
            c = conn.cursor()
            c.execute("""
                INSERT INTO transactions (date, amount, category, type, description)
                VALUES (?, ?, ?, ?, ?)
            """, (t_date, amt, t_cat, t_type, t_desc))
            conn.commit()
        except Exception as e:
            print("Insert error:", e)
        finally:
            conn.close()

        flash("Transaction saved.", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_transaction.html")

# AI insights
@app.route("/insights")
def insights():
    conn = sqlite3.connect("finance.db")

    try:
        # Get all transactions
        df = pd.read_sql("SELECT * FROM transactions", conn)

        if df.empty:
            return render_template("insights.html",
                                 total_income=0,
                                 total_expenses=0,
                                 balance=0,
                                 savings_rate=0,
                                 tips=["Add more transactions to get personalized tips."])

        # Calculate basic financials - FIXED CASE SENSITIVITY
        total_income = df[df['type'].str.lower() == 'income']['amount'].sum()
        total_expenses = df[df['type'].str.lower() == 'expense']['amount'].sum()
        balance = total_income - total_expenses
        savings_rate = (balance / total_income * 100) if total_income > 0 else 0

        # Generate FRESH tips - no accumulation
        tips = []
        if savings_rate < 20:
            tips.append("Try to save at least 20% of your income")
        elif savings_rate > 50:
            tips.append("Excellent savings rate! Consider investing")
        else:
            tips.append("Good financial habits! Keep it up")

        if total_expenses > total_income * 0.6:
            tips.append("Your expenses are high relative to income")

        if len(tips) == 0:
            tips.append("Add more transactions for personalized advice")

        return render_template("insights.html",
                             total_income=total_income,
                             total_expenses=total_expenses,
                             balance=balance,
                             savings_rate=round(savings_rate, 1),
                             tips=tips)

    except Exception as e:
        print("Insights error:", e)
        return render_template("insights.html",
                             total_income=0,
                             total_expenses=0,
                             balance=0,
                             savings_rate=0,
                             tips=["System error. Please try again."])
    finally:
        conn.close()


# Simple APIs

@app.route("/api/transactions")
def api_transactions():
    conn = sqlite3.connect("finance.db")
    df = pd.read_sql("SELECT * FROM transactions ORDER BY date DESC", conn)
    conn.close()
    return jsonify(df.to_dict("records"))

@app.route("/api/summary")
def api_summary():
    conn = sqlite3.connect("finance.db")
    df = pd.read_sql("""
        SELECT strftime('%Y-%m', date) AS month,
               type,
               SUM(amount) AS total
        FROM transactions
        GROUP BY month, type
        ORDER BY month
    """, conn)
    conn.close()
    return jsonify(df.to_dict("records"))


# DELETE TRANSACTION ROUTE
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    conn = None
    try:
        conn = sqlite3.connect("finance.db")
        c = conn.cursor()
        c.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        flash("Transaction deleted successfully!", "success")
    except Exception as e:
        print("Delete error:", e)
        if conn:
            conn.rollback()
        flash("Error deleting transaction!", "danger")
    finally:
        if conn:
            conn.close()

    return redirect(url_for("dashboard"))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
