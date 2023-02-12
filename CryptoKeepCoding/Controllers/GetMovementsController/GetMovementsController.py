from flask import jsonify, json
from sqlite3 import Error
from ..Db.db import get_db_connection
from ...Models.Movement import Movement

def get_movements():
    response = []
    status_code: int
    try: 
        movements = fetch_movements()
        response = {"status": "success", "data": json.loads(json.dumps(movements, default=vars))} 
        status_code = 200
    except Error as er:
        print(str(er))
        response = {"status": "fail", "mensaje": str(er)}
        status_code = 400
    return jsonify(response), status_code

def fetch_movements():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM movements').fetchall()
    conn.close()
    movements = []
    for row in rows:
        movement = Movement(row["id"], row["date"], row["time"], row["moneda_from"], row["cantidad_from"], row["moneda_to"], row["cantidad_to"])
        movements.append(movement)
    return movements