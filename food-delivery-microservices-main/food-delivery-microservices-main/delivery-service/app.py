from flask import Flask, request

app = Flask(__name__)


# Sample delivery data
deliveries = [
    {
        "delivery_id": 9001,
        "order_id": 501,
        "restaurant_id": 101,
        "delivery_person": None,
        "status": "PENDING"
    },
    {
        "delivery_id": 9002,
        "order_id": 502,
        "restaurant_id": 102,
        "delivery_person": "Ravi",
        "status": "ASSIGNED"
    }
]


# Allowed delivery statuses
ALLOWED_STATUSES = [
    "PENDING",
    "ASSIGNED",
    "PICKED_UP",
    "OUT_FOR_DELIVERY",
    "DELIVERED"
]


# Valid status transitions
STATUS_TRANSITIONS = {
    "PENDING": "ASSIGNED",
    "ASSIGNED": "PICKED_UP",
    "PICKED_UP": "OUT_FOR_DELIVERY",
    "OUT_FOR_DELIVERY": "DELIVERED"
}


# Home route
@app.route("/")
def home():
    return "Delivery Service is running"


# API 1: Create a delivery
@app.route("/deliveries", methods=["POST"])
def create_delivery():

    data = request.get_json()

    if not data:
        return {"error": "Request body is required"}, 400

    if "order_id" not in data:
        return {"error": "order_id is required"}, 400

    if "restaurant_id" not in data:
        return {"error": "restaurant_id is required"}, 400

    # Generate a new delivery ID
    new_delivery_id = max(
        delivery["delivery_id"] for delivery in deliveries
    ) + 1

    new_delivery = {
        "delivery_id": new_delivery_id,
        "order_id": data["order_id"],
        "restaurant_id": data["restaurant_id"],
        "delivery_person": None,
        "status": "PENDING"
    }

    deliveries.append(new_delivery)

    return new_delivery, 201


# API 2: Get delivery details
@app.route("/deliveries/<int:delivery_id>", methods=["GET"])
def get_delivery(delivery_id):

    for delivery in deliveries:
        if delivery["delivery_id"] == delivery_id:
            return delivery

    return {"error": "Delivery not found"}, 404


# API 3: Assign delivery person
@app.route("/deliveries/<int:delivery_id>/assign", methods=["PUT"])
def assign_delivery_person(delivery_id):

    delivery = None

    for item in deliveries:
        if item["delivery_id"] == delivery_id:
            delivery = item
            break

    if delivery is None:
        return {"error": "Delivery not found"}, 404

    data = request.get_json()

    if not data or "delivery_person" not in data:
        return {"error": "delivery_person is required"}, 400

    if not data["delivery_person"]:
        return {"error": "delivery_person cannot be empty"}, 400

    # Assignment is allowed only when delivery is PENDING
    if delivery["status"] != "PENDING":
        return {
            "error": "Delivery person can only be assigned to a PENDING delivery"
        }, 400

    delivery["delivery_person"] = data["delivery_person"]
    delivery["status"] = "ASSIGNED"

    return delivery


# API 4: Update delivery status
@app.route("/deliveries/<int:delivery_id>/status", methods=["PUT"])
def update_delivery_status(delivery_id):

    delivery = None

    for item in deliveries:
        if item["delivery_id"] == delivery_id:
            delivery = item
            break

    if delivery is None:
        return {"error": "Delivery not found"}, 404

    data = request.get_json()

    if not data or "status" not in data:
        return {"error": "status is required"}, 400

    new_status = data["status"]

    # Check whether status is valid
    if new_status not in ALLOWED_STATUSES:
        return {
            "error": "Invalid status",
            "allowed_statuses": ALLOWED_STATUSES
        }, 400

    current_status = delivery["status"]

    # Prevent changing from DELIVERED
    if current_status == "DELIVERED":
        return {
            "error": "Delivery is already DELIVERED"
        }, 400

    # Check valid status transition
    expected_status = STATUS_TRANSITIONS.get(current_status)

    if new_status != expected_status:
        return {
            "error": "Invalid status transition",
            "current_status": current_status,
            "expected_status": expected_status
        }, 400

    # A delivery must have a delivery person before PICKED_UP
    if new_status == "PICKED_UP" and delivery["delivery_person"] is None:
        return {
            "error": "Delivery person must be assigned before pickup"
        }, 400

    delivery["status"] = new_status

    return delivery


# API 5: Check delivery status
@app.route("/deliveries/<int:delivery_id>/status", methods=["GET"])
def get_delivery_status(delivery_id):

    for delivery in deliveries:
        if delivery["delivery_id"] == delivery_id:
            return {
                "delivery_id": delivery["delivery_id"],
                "status": delivery["status"]
            }

    return {"error": "Delivery not found"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)