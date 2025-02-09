from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify("Shipping Company Simulation")


@app.route("/simulate_shipping_company/", methods=["POST"])
def simulate_shipping_company():
    data = request.json
    order_details = data["product_details"]
    buyer_email = data["buyer_email"]
    seller_email = data["seller_email"]

    auth_header = request.headers.get("Authorization")
    if auth_header != "1234567890abcdef":
        return jsonify({"error": "Unauthorized"}), 401

    shipping_response = (
        f"Order {order_details['order_number']} has been shipped successfully"
    )

    respon = {
        "shipping_response": shipping_response,
        "order_details": order_details,
        "status": "Shipped",
    }

    return jsonify(respon), 200


@app.route("/simulate_failed_shipping_company/", methods=["POST"])
def simulate_failed_shipping_company():
    data = request.json
    order_details = data["product_details"]
    buyer_email = data["buyer_email"]
    seller_email = data["seller_email"]

    auth_header = request.headers.get("Authorization")
    if auth_header != "1234567890abcdef":
        return jsonify({"error": "Unauthorized"}), 401

    shipping_response = (
        f"Order {order_details['order_number']} has failed to be shipped"
    )

    respon = {
        "shipping_response": shipping_response,
        "order_details": order_details,
        "status": "Failed",
    }

    return jsonify(respon), 200


if __name__ == "__main__":
    app.run(debug=True)
