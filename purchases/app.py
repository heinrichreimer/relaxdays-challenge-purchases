from flask import Flask, jsonify, request, Response
from flasgger import Swagger, swag_from
from typing import List, Dict
from purchases.purchase import Purchase
from distance import levenshtein

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
@swag_from("./add_purchase.yml", validation=True)
def add_purchase():
    purchases.append(dict_to_purchase(request.json))
    return ""


@app.route("/purchases", methods=["GET"])
@swag_from("./get_purchases.yml")
def get_purchases():
    result = purchases
    result = list(map(purchase_to_dict, result))
    return jsonify(result)


@app.route("/purchasesForArticle", methods=["GET"])
@swag_from("./get_purchases_for_article.yml")
def get_purchases_for_article():
    if "x" not in request.args:
        return Response("Must specify article ID.", status=400)
    article_id = int(request.args["x"])

    result = purchases
    result = list(filter(
        lambda purchase: purchase.article_id == article_id, result
    ))
    result = list(map(purchase_to_dict, result))
    return jsonify(result)


@app.route("/searchLieferant", methods=["GET"])
@swag_from("./search_supplier.yml")
def search_supplier():
    if "x" not in request.args:
        return Response("Must specify query.", status=400)
    query = request.args["x"]

    result = purchases
    result = list(map(
        lambda purchase: [levenshtein(purchase.supplier, query), purchase],
        result
    ))
    result = list(filter(
        lambda dist_purchase: dist_purchase[0] <= 10,
        result
    ))
    result.sort(
        key=lambda dist_purchase: dist_purchase[0],
    )
    result = list(map(
        lambda dist_purchase: dist_purchase[1].supplier,
        result
    ))
    return jsonify(result)
