from flask import Flask, request, jsonify
from flasgger import Swagger
import requests

app = Flask(__name__)
swagger = Swagger(app)

# Other microservices
RESTAURANT_SERVICE_URL = "http://restaurant-service:5000"
DELIVERY_SERVICE_URL = "http://delivery-service:5001"

# Simple in-memory order storage
orders = {
    501: {
        "order_id": 501,
        "restaurant_id": 101,
        "items": [
            {
                "item_id": 2,
                "quantity": 2
            }
        ],
        "customer_id": 1,
        "status": "PLACED"
    }
}

# Allowed order statuses
ORDER_STATUSES = [
    "PLACED",
    "CONFIRMED",
    "PREPARING",
    "READY_FOR_PICKUP",
    "OUT_FOR_DELIVERY",
    "DELIVERED"
]


# 1. Create a new order
@app.route("/orders", methods=["POST"])
def create_order():
    """
    Create a new order and communicate with Restaurant
    and Delivery services.
    ---
    tags:
      - Orders
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: order
        required: true
        schema:
          type: object
          required:
            - restaurant_id
            - items
            - customer_id
          properties:
            restaurant_id:
              type: integer
              example: 101
            items:
              type: array
              items:
                type: object
                properties:
                  item_id:
                    type: integer
                    example: 2
                  quantity:
                    type: integer
                    example: 2
            customer_id:
              type: integer
              example: 1
    responses:
      201:
        description: Order created successfully
      400:
        description: Invalid request
      503:
        description: Microservice unavailable
    """

    data = request.get_json()

    # Basic request validation
    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = [
        "restaurant_id",
        "items",
        "customer_id"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    if not isinstance(data["items"], list) or len(data["items"]) == 0:
        return jsonify({
            "error": "items must be a non-empty list"
        }), 400

    restaurant_id = data["restaurant_id"]

    # ---------------------------------------------------------
    # STEP 1: Communicate with Restaurant Service
    # ---------------------------------------------------------

    try:
        restaurant_response = requests.get(
            f"{RESTAURANT_SERVICE_URL}/restaurants/{restaurant_id}",
            timeout=5
        )
    except requests.RequestException:
        return jsonify({
            "error": "Restaurant Service is unavailable"
        }), 503

    if restaurant_response.status_code != 200:
        return jsonify({
            "error": "Restaurant not found"
        }), 400

    restaurant = restaurant_response.json()

    # Check restaurant availability
    if not restaurant.get("available"):
        return jsonify({
            "error": "Restaurant is not available"
        }), 400

    # ---------------------------------------------------------
    # STEP 2: Check ordered items through Restaurant Service
    # ---------------------------------------------------------

    for item in data["items"]:

        item_id = item.get("item_id")

        if item_id is None:
            return jsonify({
                "error": "item_id is required"
            }), 400

        try:
            item_response = requests.get(
                f"{RESTAURANT_SERVICE_URL}/restaurants/"
                f"{restaurant_id}/menu/{item_id}",
                timeout=5
            )
        except requests.RequestException:
            return jsonify({
                "error": "Restaurant Service is unavailable"
            }), 503

        if item_response.status_code != 200:
            return jsonify({
                "error": f"Item {item_id} not found"
            }), 400

        menu_item = item_response.json()

        # Check item availability
        if not menu_item.get("available"):
            return jsonify({
                "error": f"Item {item_id} is not available"
            }), 400

    # ---------------------------------------------------------
    # STEP 3: Create the order
    # ---------------------------------------------------------

    new_order_id = max(orders.keys()) + 1

    new_order = {
        "order_id": new_order_id,
        "restaurant_id": restaurant_id,
        "items": data["items"],
        "customer_id": data["customer_id"],
        "status": "PLACED"
    }

    orders[new_order_id] = new_order

    # ---------------------------------------------------------
    # STEP 4: Communicate with Delivery Service
    # ---------------------------------------------------------

    try:
        delivery_response = requests.post(
            f"{DELIVERY_SERVICE_URL}/deliveries",
            json={
                "order_id": new_order_id,
                "restaurant_id": restaurant_id
            },
            timeout=5
        )
    except requests.RequestException:
        return jsonify({
            "error": "Delivery Service is unavailable",
            "order": new_order
        }), 503

    if delivery_response.status_code not in [200, 201]:
        return jsonify({
            "error": "Failed to create delivery",
            "order": new_order
        }), 500

    delivery = delivery_response.json()

    # ---------------------------------------------------------
    # STEP 5: Return combined response
    # ---------------------------------------------------------

    return jsonify({
        "message": "Order created successfully",
        "order": new_order,
        "restaurant": restaurant,
        "delivery": delivery
    }), 201


# 2. Get an order
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """
    Get an order by ID
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        required: true
        type: integer
        example: 501
    responses:
      200:
        description: Order found successfully
      404:
        description: Order not found
    """

    order = orders.get(order_id)

    if order is None:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify(order), 200


# 3. Update order status
@app.route("/orders/<int:order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    """
    Update order status
    ---
    tags:
      - Orders
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: order_id
        in: path
        required: true
        type: integer
        example: 501
      - in: body
        name: status
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum:
                - PLACED
                - CONFIRMED
                - PREPARING
                - READY_FOR_PICKUP
                - OUT_FOR_DELIVERY
                - DELIVERED
              example: CONFIRMED
    responses:
      200:
        description: Order status updated successfully
      400:
        description: Invalid status or request
      404:
        description: Order not found
    """

    order = orders.get(order_id)

    if order is None:
        return jsonify({
            "error": "Order not found"
        }), 404

    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({
            "error": "status is required"
        }), 400

    new_status = data["status"]

    if new_status not in ORDER_STATUSES:
        return jsonify({
            "error": "Invalid status",
            "allowed_statuses": ORDER_STATUSES
        }), 400

    order["status"] = new_status

    return jsonify(order), 200


# Start the Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)