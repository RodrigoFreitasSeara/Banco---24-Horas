from __future__ import annotations
from cliente import Cliente
from movimentacao import Movimentacao
from decimal import Decimal


class Conta:
    contasCriadas = 0

    def __init__(self, titular: Cliente, numero: int):
        Conta.contasCriadas += 1

        self.titular = titular
        self.numeroConta = Conta.contasCriadas
        self._saldo = Decimal("0.00")
        self.historicoMovimentacoes = HistoricoMovimentacoes()

    def __repr__(self) -> str:
        return (
            f"Conta(titular={self.titular!r}, "
            f"numeroDaConta={self.numeroConta!r}, "
            f"saldo={self._saldo!r},)"
        )

    @property
    def saldo(self) -> Decimal:
        return self._saldo

    def depositar(self, valor: float) -> None:
        self.creditar(valor)
        self.historicoMovimentacoes.append(Movimentacao("Depósito", valor))

    def sacar(self, valor: float) -> None:
            self.debitar(valor)
            self.historicoMovimentacoes.append(Movimentacao("Saque", valor))

    def extrato(self) -> None:
        print(f"Extrato - Conta {self.numeroConta} - Titular: {self.titular.nome}")
        self.historicoMovimentacoes.imprimir_extrato()


    def creditar(self, valor: float):
        """creditar deve ser usado apenas através da classe controladora de transações bancárias"""
        v: Decimal = Decimal(str(valor))
        if v <= Decimal("0.00"):
            raise ValueError("Não se pode creditar um valor negativo ou nulo a uma conta")

        self._saldo += v
    

    def debitar(self, valor: float):
        """creditar deve ser usado apenas através da classe controladora de transações bancárias """
        v: Decimal = Decimal(str(valor))
        if v <= Decimal("0.00"):
            raise ValueError("Não se pode debitar um valor negativo ou nulo a uma conta")
        
        if v > self._saldo:
            raise ValueError("Saldo insuficiente para debito em conta")

        self._saldo -= v


        

    
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


class HistoricoMovimentacoes(list):
    def imprimir_extrato(self) -> None:
        print(f"{'Data/Hora':<20} | {'Tipo':<10} | {'Valor':>13} | {'Saldo':>13}")
        print("-" * 68)
        saldo = Decimal("0.00")
        for m in self:
            v = Decimal(str(m.valor))
            saldo += v if m.tipo == "Depósito" else -v
            print(
                f"{m.data_hora:<20} | {m.tipo:<10} | "
                f"R$ {m.valor:>10.2f} | R$ {float(saldo):>10.2f}"
            )
        print("-" * 68)
        print(f"{'Saldo atual:':<38} R$ {float(saldo):>10.2f}")

