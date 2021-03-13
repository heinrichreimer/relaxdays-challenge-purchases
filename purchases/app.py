from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from typing import List
from purchases.purchase import Purchase

app = Flask(__name__)
swagger = Swagger(app)
purchases: List[Purchase] = []


@app.route("/", methods=["POST"])
@swag_from("add_purchase_spec.yml", validation=True)
def add_purchase():
    purchase = Purchase(
        request.json["lieferant"],
        request.json["articleID"],
        request.json["menge"],
    )
    purchases.append(purchase)
    return ""


@app.route("/", methods=["GET"])
@swag_from("get_purchases_spec.yml")
def get_purchases():
    results = [
        {
            "lieferant": purchase.supplier,
            "articleID": purchase.article_id,
            "menge": purchase.amount,
        }
        for purchase in purchases
    ]
    return jsonify(results)
