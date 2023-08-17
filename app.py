from flask import Flask, request, jsonify
import uuid
import math
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# In-memory data storage to hold receipt information
receipts = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    """Processes the receipt data to calculate and store points."""

    # Extract data from the request payload
    data = request.json
    # Generate a unique ID for the receipt
    receipt_id = str(uuid.uuid4())

    # Calculate the points for the receipt
    points = calculate_points(data)
    # Store the calculated points against the receipt ID
    receipts[receipt_id] = points

    return jsonify({"id": receipt_id})

@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    """Returns the points for a given receipt ID."""

    # Fetch points for the provided receipt ID
    points = receipts.get(id, None)

    # Return an error if receipt is not found
    if points is None:
        return jsonify({"error": "Receipt not found"}), 404
    
    return jsonify({"points": points})

def calculate_points(data):
    """Calculates the points for the receipt based on defined rules."""

    points = 0
    
    # One point for every alphanumeric character in the retailer name
    retailer_name = data.get("retailer", "")
    points += sum([1 for char in retailer_name if char.isalnum()])

    # 50 points if the total is a round dollar amount with no cents
    total = float(data.get("total", 0.0))
    if total == round(total):
        points += 50

    # 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # 5 points for every two items on the receipt
    items = data.get("items", [])
    points += (len(items) // 2) * 5

    # If the trimmed length of the item description is a multiple of 3, 
    # multiply the price by 0.2 and round up to the nearest integer
    for item in items:
        description = item.get("shortDescription", "").strip()
        price = float(item.get("price", 0.0))
        if len(description) % 3 == 0:
            points += math.ceil(price * 0.2)

    # 6 points if the day in the purchase date is odd
    purchase_date = data.get("purchaseDate", "")
    day = datetime.strptime(purchase_date, "%Y-%m-%d").day
    if day % 2 == 1:
        points += 6

    # 6 points if the day in the purchase date is odd
    purchase_time = data.get("purchaseTime", "")
    hour = int(purchase_time.split(":")[0])
    if 14 <= hour < 16:
        points += 10

    return points

if __name__ == "__main__":
    # Start the Flask application on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
