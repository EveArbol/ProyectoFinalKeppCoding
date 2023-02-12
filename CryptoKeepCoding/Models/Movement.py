class Movement:
    def __init__(self, id: int, fecha: str, hora: str, from_moneda: str, from_cantidad: float, to_moneda: str, to_cantidad: float) -> None:
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.from_moneda = from_moneda
        self.from_cantidad = from_cantidad
        self.to_moneda = to_moneda
        self.to_cantidad = to_cantidad