from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import time
import csv
import os
import matplotlib.pyplot as plt
import google.generativeai as genai

app = Flask(__name__)

# Gemini API
genai.configure(api_key="your api key")
model = genai.GenerativeModel("gemini-2.5-flash")

chat_history = []

# -----------------------------
# SQL QUERY FUNCTION
# -----------------------------

def run_query(intent):

    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    if intent == "total_revenue":
        query = """
        SELECT SUM(sales_amount)
        FROM sales_data
        """

    elif intent == "yearly_sales":
        query = """
        SELECT strftime('%Y', order_date) AS year,
        SUM(sales_amount)
        FROM sales_data
        GROUP BY year
        """

    elif intent == "monthly_sales":
        query = """
        SELECT strftime('%m', order_date) AS month,
        SUM(sales_amount)
        FROM sales_data
        GROUP BY month
        """

    elif intent == "sales_by_region":
        query = """
        SELECT region,
        SUM(sales_amount)
        FROM sales_data
        GROUP BY region
        """

    elif intent == "category_sales":
        query = """
        SELECT product_category,
        SUM(sales_amount)
        FROM sales_data
        GROUP BY product_category
        """

    elif intent == "top_products":
        query = """
        SELECT product_name,
        SUM(sales_amount) AS total_sales
        FROM sales_data
        GROUP BY product_name
        ORDER BY total_sales DESC
        LIMIT 5
        """

    elif intent == "promo_sales":
        query = """
        SELECT promo_offer,
        SUM(sales_amount)
        FROM sales_data
        GROUP BY promo_offer
        """

    elif intent == "total_transactions":
        query = """
        SELECT COUNT(DISTINCT transaction_id)
        FROM sales_data
        """

    else:
        conn.close()
        return []

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    return result
# -----------------------------
# CHART CREATION
# -----------------------------

def create_chart(intent, result):

    if not os.path.exists("static"):
        os.makedirs("static")

    if intent == "yearly_sales":

        years = [row[0] for row in result]
        sales = [row[1] for row in result]

        plt.figure()
        plt.bar(years, sales)
        plt.title("Yearly Sales")
        plt.xlabel("Year")
        plt.ylabel("Sales")

        chart_path = "static/yearly_sales.png"
        plt.savefig(chart_path)
        plt.close()

        return chart_path


    if intent == "category_sales":

        categories = [row[0] for row in result]
        sales = [row[1] for row in result]

        plt.figure()
        plt.pie(sales, labels=categories, autopct='%1.1f%%')
        plt.title("Category Sales")

        chart_path = "static/category_sales.png"
        plt.savefig(chart_path)
        plt.close()

        return chart_path

    return None


# -----------------------------
# INTENT DETECTION
# -----------------------------

def detect_intent(question):

    prompt = f"""
    Identify the intent of the retail analytics question.

    Possible intents:
    total_revenue
    yearly_sales
    monthly_sales
    sales_by_region
    category_sales
    top_products
    promo_sales
    total_transactions

    Question: {question}

    Return ONLY the intent name from the list above.
    Do not explain anything.
    """

    try:
        response = model.generate_content(prompt)
        intent = response.text.strip().lower()
    except:
        intent = "total_revenue"

    return intent


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------
# CHAT ROUTE
# -----------------------------

@app.route("/chat", methods=["POST"])
def chat():

    start = time.time()

    data = request.json
    question = data["message"]

    intent = detect_intent(question)

    result = run_query(intent)

    chart = create_chart(intent, result)

    prompt = f"""
    You are a retail analytics assistant.

    Explain the sales insight in ONLY 2 short lines.
    Use simple business language.
    Do NOT explain Python lists, tuples, or database structures.

    Data: {result}
    """

    try:
        response = model.generate_content(prompt)
        explanation = response.text
    except:
        explanation = "AI explanation temporarily unavailable due to API limit."

    processing_time = round(time.time() - start, 2)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    chat_history.append({
        "question": question,
        "answer": explanation,
        "timestamp": timestamp,
        "processing_time": processing_time
    })

    return jsonify({
        "explanation": explanation,
        "processing_time": processing_time,
        "chart": chart,
        "history": chat_history
    })


# -----------------------------
# DOWNLOAD REPORT
# -----------------------------

@app.route("/download")
def download_report():

    filename = "chat_report.csv"

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Question",
            "Answer",
            "Timestamp",
            "Processing Time"
        ])

        for chat in chat_history:
            writer.writerow([
                chat["question"],
                chat["answer"],
                chat["timestamp"],
                chat["processing_time"]
            ])

    return send_file(filename, as_attachment=True)


# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)