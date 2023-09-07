import sqlite3
import secrets
import requests
from flask import Flask, render_template

secret_key = secrets.token_hex(16)
serpapi_api_key = "268d96d42db12c081079c5c0ee8bed74c2432e32cc88e1154a55a35640c9dbab"

app = Flask(__name__)
app.secret_key = secret_key


db_file = "crypto_data.db"
with sqlite3.connect(db_file) as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS crypto (symbol TEXT PRIMARY KEY, price TEXT)")


def fetch_crypto_data():
    crypto_symbols = [
    "BTC-USD", "ETH-USD", "XRP-USD", "LTC-USD", "BCH-USD",
    "ADA-USD", "DOGE-USD", "DOT-USD", "LINK-USD", "MATIC-USD"
]

    data = []

    for symbol in crypto_symbols:
        url = f"https://serpapi.com/search.json?engine=google_finance&q={symbol}&api_key={serpapi_api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data_json = response.json()
            price = data_json.get("summary", {}).get("price")

            if price:
                data.append({
                    "name": symbol,
                    "price": price.strip("$")
                })

        except:
            print("Unsuccessful")

    return data


def insert_crypto_data(data):
    db_file = "crypto_data.db"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        data_tuples = [(crypto["name"], crypto["price"]) for crypto in data]

        cursor.executemany("INSERT OR REPLACE INTO crypto (symbol, price) VALUES (?, ?)", data_tuples)
        conn.commit()


@app.route("/")
def index():
    crypto_data = fetch_crypto_data()
    insert_crypto_data(crypto_data)
    with sqlite3.connect("crypto_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT symbol, price FROM crypto")
        crypto_data = cursor.fetchall()

    return render_template("index.html", crypto_data=crypto_data)




if __name__ == "__main__":
    app.run(debug=True)
