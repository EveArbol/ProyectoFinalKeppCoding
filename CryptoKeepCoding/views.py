from CryptoKeepCoding import app
from flask import render_template, request
from .Controllers.GetMovementsController.GetMovementsController import get_movements as movements
from .Controllers.GetStatusController.GetStatusController import get_status as status
from .Controllers.GetExchangeRateController.GetExchangeRateController import get_exchange_rate as exchange_rate
from .Controllers.AddMovementController.AddMovementController import add_movement

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/v1/movimientos", methods=["GET"])
def get_movements():
    return movements()

@app.route("/api/v1/status", methods=["GET"])
def get_status():
    return status()

@app.route("/api/v1/tasa/<moneda_from>/<moneda_to>" , methods=["GET"])
def get_exchange_rate(moneda_from, moneda_to):
    return exchange_rate(moneda_from=moneda_from, moneda_to=moneda_to)

@app.route("/api/v1/movimiento", methods=["POST"])
def post_movement():
    return add_movement(request=request)