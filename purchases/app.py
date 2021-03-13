from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from typing import List, Dict
from purchases.purchase import Purchase

app = Flask(__name__)
swagger = Swagger(app)
purchases: List[Purchase] = []


def dict_to_purchase(purchase: Dict) -> Purchase:
    return Purchase(
        purchase["lieferant"],
        purchase["articleID"],
        purchase["menge"],
    )


def purchase_to_dict(purchase: Purchase) -> Dict:
    return {
        "lieferant": purchase.supplier,
        "articleID": purchase.article_id,
        "menge": purchase.amount,
    }


@app.route("/purchase", methods=["POST"])
@swag_from("add_purchase_spec.yml", validation=True)
def add_purchase():
    purchases.append(dict_to_purchase(request.json))
    return ""


@app.route("/purchases", methods=["GET"])
@swag_from("get_purchases_spec.yml")
def get_purchases():
    result = purchases
    result = list(map(purchase_to_dict, result))
    return jsonify(result)


@app.route("/purchasesForArticle/<articleID>", methods=["GET"])
@swag_from("get_purchases_for_article_spec.yml")
def get_purchases_for_article(articleID):

    def is_correct_article_id(purchase: Purchase):
        return purchase.article_id == int(articleID)

    result = purchases
    result = list(filter(is_correct_article_id, result))
    result = list(map(purchase_to_dict, result))
    return jsonify(result)
