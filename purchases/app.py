from flask import Flask, jsonify, request, Response
from flasgger import Swagger, swag_from
from typing import List, Dict
from purchases.purchase import Purchase
from distance import levenshtein
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)
swagger = Swagger(app)

purchases: List[Purchase] = []


def dict_to_purchase(purchase: Dict) -> Purchase:
    return Purchase(
        purchase["lieferant"],
        purchase["articleID"],
        purchase["menge"],
        Decimal(purchase["preis"]),
        datetime.now()
    )


def purchase_to_dict(purchase: Purchase) -> Dict:
    return {
        "lieferant": purchase.supplier,
        "articleID": purchase.article_id,
        "menge": purchase.amount,
        "preis": str(purchase.price),
    }


@app.route("/purchase", methods=["POST"])
@swag_from("./specs/add_purchase.yml", validation=True)
def add_purchase():
    purchases.append(dict_to_purchase(request.json))
    return ""


@app.route("/purchases", methods=["GET"])
@swag_from("./specs/get_purchases.yml")
def get_purchases():
    result = purchases
    result = list(map(purchase_to_dict, result))
    return jsonify(result)


@app.route("/purchasesForArticle", methods=["GET"])
@swag_from("./specs/get_purchases_for_article.yml")
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
@swag_from("./specs/search_supplier.yml")
def search_supplier():
    if "x" not in request.args:
        return Response("Must specify query.", status=400)
    query = request.args["x"]

    result = purchases
    result = set(map(
        lambda purchase: purchase.supplier,
        result
    ))
    result = list(map(
        lambda supplier: [levenshtein(supplier, query), supplier],
        result
    ))
    result = list(filter(
        lambda dist_supplier: dist_supplier[0] <= 10,
        result
    ))
    result.sort(
        key=lambda dist_supplier: dist_supplier[0],
    )
    result = list(map(
        lambda dist_supplier: dist_supplier[1],
        result
    ))
    return jsonify(result)


@app.route("/purchasesBetween", methods=["GET"])
@swag_from("./specs/get_purchases_between.yml")
def get_purchases_between():
    if "x" not in request.args:
        return Response("Must specify start date.", status=400)
    start_time = datetime.strptime(request.args["x"], "%d.%m.%Y %H:%M:%S")

    if "y" not in request.args:
        return Response("Must specify start date.", status=400)
    end_time = datetime.strptime(request.args["y"], "%d.%m.%Y %H:%M:%S")

    result = purchases
    result = list(filter(
        lambda purchase: purchase.time >= start_time and
        purchase.time <= end_time,
        result
    ))
    result = list(map(purchase_to_dict, result))
    return jsonify(result)
