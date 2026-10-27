from datetime import datetime


class Movimentacao:
    """Representa uma operação financeira de uma conta bancária."""

    FORMATO_DATA = "%d/%m/%Y %H:%M:%S"

    def __init__(self, tipo: str, valor: float, data_hora: str | None = None) -> None:
        self._tipo = tipo
        self._valor = valor
        if data_hora is None:
            data_hora = datetime.now().strftime(self.FORMATO_DATA)
        self._data_hora = data_hora

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def valor(self) -> float:
        return self._valor

    @property
    def data_hora(self) -> str:
        return self._data_hora

    def __str__(self) -> str:
        return f"{self._data_hora} | {self._tipo:<10} | R$ {self._valor:>10.2f}"