from flask import jsonify
from sqlite3 import Error
from ..GetMovementsController.GetMovementsController import fetch_movements
from ..GetExchangeRateController.GetExchangeRateController import get_exchange_rate

def get_status():
    response = []
    status_code: int
    data = {}
    try: 
        movements = fetch_movements()
        invested = 0
        recovered = 0
        purchase_value = 0
        current_value = 0
        currencies = {}
        for movement in movements:
            if movement.from_moneda == "EUR":
                invested += movement.from_cantidad
            if movement.to_moneda == "EUR":
                recovered += movement.to_cantidad
            if movement.from_moneda not in currencies: 
                currencies[movement.from_moneda] = 0
            if movement.to_moneda not in currencies: 
                currencies[movement.to_moneda] = 0

            currencies[movement.from_moneda] -= movement.from_cantidad
            currencies[movement.to_moneda] += movement.to_cantidad
        for key, value in currencies.items():
            if key != "EUR":
                rate = get_exchange_rate(key, "EUR")[0].json
                current_value += value * rate["rate"]

        data["invested"] = invested
        data["recovered"] = recovered
        data["purchase_value"] = invested - recovered
        data["current_value"] = current_value
        response = {"status": "success", "data": data} 
        status_code = 200
    except Error as er:
        response = {"status": "fail", "mensaje": str(er)}
        status_code = 400
    return jsonify(response), status_code