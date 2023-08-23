from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Conversion rates dictionary (USD as base currency)
conversion_rates = {
    'USD': {
        'IQD': 1540,  # 1 USD = 1500 IQD
        'EUR': 0.85   # 1 USD = 0.85 EUR (placeholder)
        # Add more conversion rates as needed
    },
    'IQD': {
        'USD': 1 / 1540  # 1 IQD = 0.00066667 USD
        # Add more conversion rates as needed
    }
}

def save_conversion(from_currency, to_currency, amount, converted_amount):
    conn = sqlite3.connect('currency_history.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversions (from_currency, to_currency, amount, converted_amount) VALUES (?, ?, ?, ?)",
                   (from_currency, to_currency, amount, converted_amount))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    currencies = list(conversion_rates.keys())
    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert():
    amount = float(request.form['amount'])
    from_currency = request.form['from_currency']
    to_currency = request.form['to_currency']

    if from_currency in conversion_rates and to_currency in conversion_rates[from_currency]:
        conversion_rate = conversion_rates[from_currency][to_currency]
        converted_amount = amount * conversion_rate
        save_conversion(from_currency, to_currency, amount, converted_amount)
    else:
        converted_amount = 0  # Unsupported conversion

    return jsonify({'converted_amount': converted_amount})

if __name__ == '__main__':
    app.run(debug=True)
