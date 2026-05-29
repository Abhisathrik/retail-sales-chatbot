#  AI-Powered Retail Sales Analytics Chatbot

A conversational analytics tool that lets you ask business questions in plain English and get instant sales insights — no SQL knowledge needed.

---

##  What This Project Does

Ever wanted to just *ask* your sales data a question instead of writing queries?

That's exactly what this does. You type something like *"What were the top selling products this year?"* and the chatbot figures out what you're asking, runs the right SQL query on the database, and gives you a clean 2-line business insight — sometimes with a chart.

I built this because I wanted to bridge the gap between raw data and real business understanding, especially for people who aren't technical but still need answers fast.

---

##  Features

- **Natural language to SQL** — type any sales question in plain English
- **Intent detection** — powered by Google Gemini AI to understand what you're really asking
- **8 query types** supported out of the box:
  - Total revenue
  - Yearly & monthly sales trends
  - Sales by region
  - Category-wise breakdown
  - Top 5 products
  - Promo offer performance
  - Total transaction count
- **Auto-generated charts** — bar and pie charts for visual queries
- **AI explanations** — Gemini summarizes every result in 2 simple business lines
- **Chat history** — tracks your full session
- **CSV export** — download your entire Q&A session as a report

---

##  Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| AI / NLP | Google Gemini AI (gemini-2.5-flash) |
| Data & ML | Pandas, Matplotlib |
| Frontend | HTML, CSS, JavaScript |

---

##  Project Structure

```
retail-sales-chatbot/
│
├── app.py                  # Main Flask app — routes, intent detection, SQL queries
├── sales.db                # SQLite database with retail sales data
├── chat_report.csv         # Auto-generated session report (created on export)
├── PROJECT_22.ipynb        # Jupyter notebook — data exploration & model testing
│
└── templates/
    └── index.html          # Frontend chat interface
```

---

##  How to Run It Locally

**1. Clone the repository**
```bash
git clone https://github.com/YOURUSERNAME/retail-sales-chatbot.git
cd retail-sales-chatbot
```

**2. Install dependencies**
```bash
pip install flask google-generativeai matplotlib pandas
```

**3. Add your Gemini API key**

Open `app.py` and replace the placeholder:
```python
genai.configure(api_key="YOUR_API_KEY_HERE")
```
Get a free key at: https://makersuite.google.com/app/apikey

**4. Run the app**
```bash
python app.py
```

**5. Open in your browser**
```
http://127.0.0.1:5000
```

---

##  Example Questions You Can Ask

- *"What is the total revenue?"*
- *"Show me yearly sales"*
- *"Which products are selling the most?"*
- *"How did promo offers perform?"*
- *"What are the sales by region?"*

---

##  Sample Output

When you ask *"Show me category sales"*, the chatbot:
1. Detects intent → `category_sales`
2. Runs the SQL query on `sales.db`
3. Generates a pie chart
4. Returns a 2-line AI business summary like:
   > *"Electronics leads category sales at 38%, followed by Clothing at 27%. These two categories together account for nearly two-thirds of total revenue."*

---

---

##  About Me

Built by **Abhi Sathrik Induru** — B.Tech IT graduate from Hyderabad, passionate about using data and AI to solve real business problems.

📧 sathrik09@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/abhisathrik)

---

## 📄 License

This project is open source and free to use for learning and portfolio purposes.

