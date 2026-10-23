from cliente import Cliente

class Conta:
    contasCriadas = 0

    def __init__(self, titular: Cliente):
        Conta.contasCriadas += 1
        
        self.titular = titular
        self.numeroConta = Conta.contasCriadas
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

    