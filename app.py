from flask import Flask, jsonify, request, g
import requests
import threading
import time
import logging
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# Global variables
exchange_rate = {
    "USD_to_BRL": None,
    "all_rates": None  
}
logs = []  # List to store log entries

# Constants
EXCHANGE_API_URL = "https://open.er-api.com/v6/latest/USD"  
FETCH_INTERVAL = 120  
LOG_RETRY_INTERVAL = 10  

# Middleware to log incoming requests
@app.before_request
def log_request():
    g.start_time = datetime.now()  
    logging.info(f"Incoming {request.method} request to {request.path}")

@app.after_request
def log_response(response):
    processing_time = (datetime.now() - g.start_time).total_seconds()
    log_entry = {
        "processing_date": g.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "processing_duration": processing_time,
        "end_processing_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": response.status,
        "endpoint": request.path,
        "method": request.method
    }
    logs.append(log_entry)  # Add log entry to the global logs
    logging.info(f"Request to {request.path} completed in {processing_time:.2f}s with status {response.status}")
    return response

# Function to fetch exchange rates
def fetch_exchange_rate(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            exchange_rate["USD_to_BRL"] = data.get("rates", {}).get("BRL", None)
            exchange_rate["all_rates"] = data.get("rates", {})  # Store all rates globally
            logging.info(f"[Global] Updated exchange rate: {exchange_rate}")
            return {"status": "success", "data": data}
        else:
            logging.error(f"[Global] Failed to fetch exchange rate. HTTP Status: {response.status_code}")
            return {"status": "error", "message": "Failed to fetch exchange rate"}
    except Exception as e:
        logging.error(f"[Global] Error fetching exchange rate: {e}")
        return {"status": "error", "message": str(e)}

# API route to get the exchange rates (GET)
@app.route("/api/exchange-rate", methods=["GET"])
def get_exchange_rate():
    return jsonify(exchange_rate)

# API route to fetch exchange rates dynamically (POST)
@app.route("/api/exchange-rate", methods=["POST"])
def fetch_exchange_rate_on_request():
    try:
        global_result = fetch_exchange_rate(EXCHANGE_API_URL)
        if global_result["status"] == "success":
            return jsonify({"status": "success", "data": exchange_rate}), 200
        else:
            return jsonify({
                "status": "error",
                "message": global_result.get("message", ""),
                "data": exchange_rate
            }), 500
    except Exception as e:
        logging.error(f"Error in dynamic fetch endpoint: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# API route to submit logs
@app.route("/api/logs", methods=["POST"])
def add_log():
    try:
        log_entry = request.get_json()
        if not log_entry:
            return jsonify({"error": "Invalid or empty log entry"}), 400
        logs.append(log_entry)
        logging.info(f"New log entry added: {log_entry}")
        return jsonify({"message": "Log entry added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding log: {e}")
        return jsonify({"error": "Failed to add log entry"}), 500

# API route to retrieve logs
@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify(logs)

# Start the background thread
def start_background_tasks():
    logging.info("Starting background task for global exchange rates...")
    thread = threading.Thread(target=lambda: fetch_exchange_rate(EXCHANGE_API_URL), name="GlobalExchangeRateThread")
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    logging.info("Starting the application...")
    start_background_tasks()
    app.run(host="0.0.0.0", port=5000)
