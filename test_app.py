import unittest
from app import app, calculate_points
import json

sample_data1 = {
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}

sample_data2 = {
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}

headers = {
    'Content-Type': 'application/json',
}

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_process_receipt_endpoint(self):
        """Test /receipts/process endpoint."""

        response = self.app.post('/receipts/process', data=json.dumps(sample_data1), headers=headers)

        # The response should be a 200 OK with a valid UUID
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json)
        self.assertRegex(response.json["id"], r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$")

    def test_get_points_endpoint(self):
        """Test /receipts/{id}/points endpoint."""

        response = self.app.post('/receipts/process', data=json.dumps(sample_data1), headers=headers)
        receipt_id = response.json["id"]

        # We get points for the given receipt ID
        response = self.app.get(f'/receipts/{receipt_id}/points')

        # The response should have the correct points value
        self.assertEqual(response.status_code, 200)
        self.assertIn("points", response.json)

    def test_calculate_points_function(self):
        """Test the logic of the calculate_points function."""

        # We calculate the points using the function
        points = calculate_points(sample_data1)

        self.assertEqual(points, 28)

if __name__ == "__main__":
    unittest.main()
