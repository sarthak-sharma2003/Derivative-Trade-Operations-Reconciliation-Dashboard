from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime
import random
import requests
import os
import schedule
import time
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load Alpha Vantage API Key from environment variable
#add
#your
#API
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'Add_your_API_Key_Here')  # Default API key for testing
BASE_URL = 'https://www.alphavantage.co/query'


# Function to fetch historical U.S. market data using Alpha Vantagess
def fetch_historical_data(symbol='AAPL'):
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    
    # Debugging Output
    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("API Response:", data)  # Print the full API response for debugging
        
        time_series = data.get('Time Series (Daily)', {})
        if not time_series:
            print("No historical data found in the API response.")
        
        historical_data = [
            {
                'date': date,
                'open': float(values['1. open']),
                'high': float(values['2. high']),
                'low': float(values['3. low']),
                'close': float(values['4. close']),
                'volume': int(values['5. volume'])
            }
            for date, values in time_series.items()
        ]
        return historical_data
    else:
        print(f"Failed to fetch historical data. Status Code: {response.status_code}")
        return []


# Function to fetch real-time trade data from Alpha Vantage
def fetch_real_time_data(symbol='AAPL'):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    
    # Debugging Output
    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("API Response:", data)  # Print the full API response for debugging
        
        time_series = data.get('Time Series (5min)', {})
        trade_data = [
            {
                'date': date,
                'tradeVolume': float(values['5. volume']),
                'paymentStatus': random.choice(['Pending', 'Completed', 'Failed']),
                'contractID': f'ISDA-{random.randint(10000, 99999)}',
                'counterparty': random.choice(['Bank A', 'Bank B', 'Bank C'])
            }
            for date, values in time_series.items()
        ]
        return trade_data
    else:
        print(f"Failed to fetch real-time data. Status Code: {response.status_code}")
        return []
    

#def fetch_real_time_data(symbol='AAPL'):
    mock_data = [
        {
            'date': '2025-02-20',
            'tradeVolume': 1000,
            'paymentStatus': 'Completed',
            'contractID': 'ISDA-12345',
            'counterparty': 'Bank A'
        }
    ]
    return mock_data


# Reconciliation Module
def reconcile_trades(trade_data):
    discrepancies = []
    for trade in trade_data:
        if trade['paymentStatus'] == 'Failed':
            discrepancies.append({
                'contractID': trade['contractID'],
                'issue': 'Payment failed',
                'counterparty': trade['counterparty']
            })
        if trade['tradeVolume'] < 1000:
            discrepancies.append({
                'contractID': trade['contractID'],
                'issue': 'Trade volume too low',
                'counterparty': trade['counterparty']
            })
    return discrepancies


# Scheduled Task for Automatic Data Pull and Reconciliation
def scheduled_tasks():
    print("Running scheduled tasks...")
    trade_data = fetch_real_time_data()
    discrepancies = reconcile_trades(trade_data)
    if discrepancies:
        print("Discrepancies found:", discrepancies)
    else:
        print("No discrepancies found.")


# Schedule the task to run every hour
schedule.every(1).hours.do(scheduled_tasks)


# Run the scheduled tasks in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


threading.Thread(target=run_scheduler).start()


# Default route for server status
@app.route('/')
def home():
    print(f"Received request at {request.url}")
    return "Backend Server is Running. Access the API endpoints at /api/trade-data, /api/historical-trade-data, /api/reconciliation"


# API endpoint for reconciliation results
@app.route('/api/reconciliation', methods=['GET'])
def get_reconciliation_data():
    print(f"Received request at {request.url}")
    trade_data = fetch_real_time_data()
    discrepancies = reconcile_trades(trade_data)
    return jsonify(discrepancies)


# API endpoint for historical data
@app.route('/api/historical-trade-data', methods=['GET'])
def get_historical_data():
    print(f"Received request at {request.url}")
    data = fetch_historical_data()
    return jsonify(data)


# API endpoint for real-time trade data
@app.route('/api/trade-data', methods=['GET'])
def get_trade_data():
    print(f"Received request at {request.url}")
    data = fetch_real_time_data()
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


