"""Aristas de mentira con la parte de la interfaz de sumolib que usan los modulos."""


class AristaFalsa:
    def __init__(self, id_, largo, forma, tipo="highway.residential", velocidad=10.0):
        self._id, self._largo, self._forma = id_, largo, forma
        self._tipo, self._velocidad = tipo, velocidad

    def getID(self):
        return self._id

    def getLength(self):
        return self._largo

    def getShape(self):
        return self._forma

    def getType(self):
        return self._tipo

    def getSpeed(self):
        return self._velocidad

    def allows(self, vclass):
        return True
