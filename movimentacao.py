from datetime import datetime
from decimal import Decimal


class Movimentacao:
    """Representa uma operação financeira de uma conta bancária."""

    FORMATO_DATA = "%d/%m/%Y %H:%M:%S"

    def __init__(
        self,
        tipo: str,
        valor: float | Decimal,
        direcao: str | None = None,
        data_hora: str | None = None,
    ) -> None:
        self._tipo = tipo
        self._valor = float(valor)
        if direcao is None:
            t = tipo.lower()
            if any(term in t for term in ("saque", "enviad", "débito", "debito")):
                direcao = "Débito"
            else:
                direcao = "Crédito"
        self._direcao = direcao
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
    def direcao(self) -> str:
        return self._direcao

    @property
    def data_hora(self) -> str:
        return self._data_hora

    def __str__(self) -> str:
        sinal = "+" if self._direcao == "Crédito" else "-"
        return f"{self._data_hora} | {self._tipo:<28} | {self._direcao:<7} | {sinal}R$ {self._valor:>10.2f}"
