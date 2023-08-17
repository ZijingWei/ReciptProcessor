# Receipt Processor API #
The Receipt Processor is a web service that processes receipts and calculates points based on specific rules. The service accepts receipt data in JSON format and assigns a unique ID to each processed receipt. Users can then query the service using this ID to fetch the calculated points.

## Table of Contents ##
- Installation
- Usage
- Process Receipts
- Get Points
- Points Calculation Rules
- Testing

## Installation ##
Ensure you have Docker installed before proceeding.
1. Clone the repository:
``` git clone https://github.com/ZijingWei/ReciptProcessor.git ```
2. Navigate to the repository directory:
``` cd path/to/receipt-processor ```
3. Build the Docker image:
``` docker build -t receipt-processor . ```
4. Run the Docker container:
``` docker run -p 5000:5000 receipt-processor ```
The application should now be running on `http://localhost:5000`.

## Usage ##

### Process Receipts ###
- Endpoint: `/receipts/process`
- Method: POST
- Payload: Receipt JSON
- Response: JSON containing a unique ID for the receipt.

**Example Request:**
``` curl -X POST http://localhost:5000/receipts/process -H "Content-Type: application/json" -d '{"retailer": "Target", "purchaseDate": "2022-01-01", ... }' ```
**Example Request:**
```
{
  "id": "7fb1377b-b223-49d9-a31a-5a02701dd310"
}
```

### Get Points ###
- Endpoint: `/receipts/{id}/points`
- Method: GET
- Payload: Receipt JSON
- Response: JSON containing a unique ID for the receipt.

**Example Request:**
``` curl http://localhost:5000/receipts/7fb1377b-b223-49d9-a31a-5a02701dd310/points ```
**Example Request:**
```
{
  "points": 32
}
```

## Points Calculation Rules ##
1. **Retailer Name:** One point for every alphanumeric character.
2. **Total Amount:**
    - 50 points if round dollar amount with no cents.
    - 25 points if multiple of 0.25.
3. **Items:**
    - 5 points for every two items.
    - If item description length (trimmed) is a multiple of 3, multiply the price by 0.2 and round up.
4. **Purchase Date:** 6 points if the day is odd.
5. **Purchase Time:** 10 points if between 2:00 pm and 4:00 pm.

## Testing ##
To run unit tests:
1. **Build the Docker image** 
``` docker build -t receipt-processor . ```
2. **Run the tests:**
``` docker run -e RUN_TESTS=true receipt-processor ```

