from flask import request, jsonify
from sqlite3 import Error
from ..Db.db import get_db_connection
from ...Models.Movement import Movement
from ..GetMovementsController.GetMovementsController import fetch_movements

def add_movement(request: request):
    movement = Movement(0, **request.json)
    conn = get_db_connection()
    response = {}
    status_code: int
    movements = fetch_movements()
    if(movement.from_moneda != "EUR"):
        balance = 0
        for mov in movements:
            if(mov.to_moneda == movement.from_moneda):
                balance += mov.to_cantidad
            if (mov.from_moneda == movement.from_moneda):
                balance -= mov.from_cantidad
        if (balance - float(movement.from_cantidad) <= 0):
            response = {"status": "fail", "mensaje": "Saldo insuficiente"}
            status_code = 200
            conn.close()
            return jsonify(response), status_code
    try:
        rows = conn.execute("INSERT INTO movements (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (?, ?, ?, ?, ?, ?)",
            (movement.fecha, movement.hora, movement.from_moneda, movement.from_cantidad, movement.to_moneda, movement.to_cantidad))
        conn.commit()
        response = {"status": "success", "id": rows.lastrowid, "monedas": [movement.from_moneda, movement.to_moneda]} 
        status_code = 201
    except Error as er:
        conn.rollback()
        response = {"status": "fail", "mensaje": str(er)}
        status_code = 400
    conn.close()
    return jsonify(response), status_code