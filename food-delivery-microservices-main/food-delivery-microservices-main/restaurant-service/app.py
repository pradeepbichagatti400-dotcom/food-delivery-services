from flask import Flask

app = Flask(__name__)


# Restaurant and menu sample data
restaurants = [
    {
        "restaurant_id": 101,
        "name": "Pizza House",
        "location": "Hubli",
        "available": True,
        "menu": [
            {
                "item_id": 1,
                "name": "Margherita Pizza",
                "price": 250,
                "available": True
            },
            {
                "item_id": 2,
                "name": "Farmhouse Pizza",
                "price": 300,
                "available": True
            },
            {
                "item_id": 3,
                "name": "Garlic Bread",
                "price": 150,
                "available": False
            }
        ]
    },
    {
        "restaurant_id": 102,
        "name": "South Indian Kitchen",
        "location": "Hubli",
        "available": True,
        "menu": []
    }
]


# Home route
@app.route("/")
def home():
    return "Restaurant Service is running"


# API 1: Get all restaurants
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    return restaurants


# API 2: Get a specific restaurant
@app.route("/restaurants/<int:restaurant_id>", methods=["GET"])
def get_restaurant(restaurant_id):
    for restaurant in restaurants:
        if restaurant["restaurant_id"] == restaurant_id:
            return restaurant

    return {"error": "Restaurant not found"}, 404


# API 3: Get restaurant menu
@app.route("/restaurants/<int:restaurant_id>/menu", methods=["GET"])
def get_restaurant_menu(restaurant_id):
    for restaurant in restaurants:
        if restaurant["restaurant_id"] == restaurant_id:
            return restaurant["menu"]

    return {"error": "Restaurant not found"}, 404


# API 4: Get a specific menu item
@app.route("/restaurants/<int:restaurant_id>/menu/<int:item_id>", methods=["GET"])
def get_menu_item(restaurant_id, item_id):
    for restaurant in restaurants:
        if restaurant["restaurant_id"] == restaurant_id:

            for item in restaurant["menu"]:
                if item["item_id"] == item_id:
                    return item

            return {"error": "Menu item not found"}, 404

    return {"error": "Restaurant not found"}, 404


# API 5: Get restaurant availability
@app.route("/restaurants/<int:restaurant_id>/availability", methods=["GET"])
def get_restaurant_availability(restaurant_id):
    for restaurant in restaurants:
        if restaurant["restaurant_id"] == restaurant_id:
            return {
                "restaurant_id": restaurant["restaurant_id"],
                "available": restaurant["available"]
            }

    return {"error": "Restaurant not found"}, 404


# API 6: Get menu item availability
@app.route(
    "/restaurants/<int:restaurant_id>/menu/<int:item_id>/availability",
    methods=["GET"]
)
def get_menu_item_availability(restaurant_id, item_id):
    for restaurant in restaurants:
        if restaurant["restaurant_id"] == restaurant_id:

            for item in restaurant["menu"]:
                if item["item_id"] == item_id:
                    return {
                        "restaurant_id": restaurant_id,
                        "item_id": item_id,
                        "available": item["available"]
                    }

            return {"error": "Menu item not found"}, 404

    return {"error": "Restaurant not found"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)