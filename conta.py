from cliente import Cliente
from movimentacao import Movimentacao


class Conta:
    def __init__(self, titular: Cliente, numero: int):
        self.titular = titular
        self.numeroConta = numero
        self.__saldo = 0.0
        self.historicoMovimentacoes = list()

    def __repr__(self) -> str:
        return (
            f"Conta(titular={self.titular!r}, "
            f"numeroDaConta={self.numeroConta!r}, "
            f"saldo={self.__saldo!r},)"
        )

    @property
    def saldo(self) -> float:
        return self.__saldo
    
    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser maior que zero.")
        self.__saldo += valor
        self.historicoMovimentacoes.append(Movimentacao("Depósito", valor))

    
class Contas:
    """ Classe para controle de todas as contas do sistema"""

    def __init__(self) -> None:
        self._contas: dict[int, Conta] = {}
        self._proximo_numero: int = 1

    def add(self, titular: Cliente) -> Conta:
        numero = self._proximo_numero
        self._proximo_numero += 1  

        nova_conta = Conta(titular, self._proximo_numero)
        self._contas[numero] = nova_conta
        return nova_conta

    def get(self, numero: int) -> "Conta | None":
        return self._contas.get(numero)

    def delete(self, numero: int) -> bool:
        if numero in self._contas:
            del self._contas[numero]
            return True
        return False

    def list(self) -> list[Conta]: 
        """Retorna uma cópia da lista de contas"""
        return list(self._contas.values())

    def __len__(self) -> int:
        return len(self._contas)

    def __iter__(self):
        return iter(self._contas.values())