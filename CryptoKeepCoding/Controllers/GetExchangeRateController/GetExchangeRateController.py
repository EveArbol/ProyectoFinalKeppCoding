from flask import jsonify
import requests

def get_exchange_rate(moneda_from, moneda_to):
    api_key = "1796DCC6-7651-4C80-8181-C794E936EF53"
    url = f"https://rest.coinapi.io/v1/exchangerate/{moneda_from}/{moneda_to}"
    headers = {'X-CoinAPI-Key' : api_key}
    try:
        response = requests.get(url, headers=headers).json()
        return jsonify({"status": "success", "rate": response["rate"], "monedas": [moneda_from, moneda_to]}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "fail", "mensaje": e})