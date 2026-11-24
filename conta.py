from __future__ import annotations
from typing import TYPE_CHECKING
from decimal import Decimal
from movimentacao import Movimentacao

# Para evitar importação circular
if TYPE_CHECKING:
    from cliente import Cliente


class Conta:
    def __init__(self, titular: Cliente, numero: int):
        self.titular = titular
        self.numeroConta = numero
        self._saldo = Decimal("0.00")
        self.historicoMovimentacoes = HistoricoMovimentacoes()

    def __repr__(self) -> str:
        return (
            f"Conta(titular={self.titular.nome!r}, "
            f"numeroConta={self.numeroConta!r}, "
            f"saldo={self._saldo!r})"
        )

    @property
    def saldo(self) -> Decimal:
        return self._saldo

    def depositar(self, valor: float | Decimal) -> None:
        v = Decimal(str(valor))
        if v <= Decimal("0.00"):
            raise ValueError("O valor de depósito deve ser estritamente positivo.")
        self._saldo += v
        self.historicoMovimentacoes.append(Movimentacao("Depósito", v, "Crédito"))

    def sacar(self, valor: float | Decimal) -> None:
        v = Decimal(str(valor))
        if v <= Decimal("0.00"):
            raise ValueError("O valor de saque deve ser estritamente positivo.")
        if v > self._saldo:
            raise ValueError("Saldo insuficiente para realizar o saque.")
        self._saldo -= v
        self.historicoMovimentacoes.append(Movimentacao("Saque", v, "Débito"))

    def creditar(self, valor: float | Decimal, descricao: str = "Crédito") -> None:
        """Credita valor à conta e registra no histórico."""
        v = Decimal(str(valor))
        if v <= Decimal("0.00"):
            raise ValueError("Não se pode creditar um valor negativo ou nulo.")
        self._saldo += v
        self.historicoMovimentacoes.append(Movimentacao(descricao, v, "Crédito"))

    def debitar(self, valor: float | Decimal, descricao: str = "Débito") -> None:
        """Debita valor da conta com validação de saldo."""
        v = Decimal(str(valor))
        if v <= Decimal("0.00"):
            raise ValueError("Não se pode debitar um valor negativo ou nulo.")
        if v > self._saldo:
            raise ValueError("Saldo insuficiente para débito em conta.")
        self._saldo -= v
        self.historicoMovimentacoes.append(Movimentacao(descricao, v, "Débito"))

    def transferir(
        self, destino: Conta, valor: float | Decimal, modalidade: str = "Transferência"
    ) -> None:
        """Transfere fundos entre duas contas de maneira coordenada."""
        v = Decimal(str(valor))
        if v <= Decimal("0.00"):
            raise ValueError("O valor da transferência deve ser estritamente positivo.")
        if destino.numeroConta == self.numeroConta:
            raise ValueError("Não é permitida transferência para a mesma conta de origem.")
        if v > self._saldo:
            raise ValueError("Saldo insuficiente para realizar a transferência.")

        self._saldo -= v
        destino._saldo += v

        self.historicoMovimentacoes.append(
            Movimentacao(f"{modalidade} enviada p/ Conta {destino.numeroConta}", v, "Débito")
        )
        destino.historicoMovimentacoes.append(
            Movimentacao(f"{modalidade} recebida da Conta {self.numeroConta}", v, "Crédito")
        )

    def extrato(self) -> None:
        print(f"\n=== Extrato - Conta nº {self.numeroConta} - Titular: {self.titular.nome} (CPF: {self.titular.cpf}) ===")
        self.historicoMovimentacoes.imprimir_extrato(saldo_atual=self._saldo)


class Contas:
    """Classe para controle de todas as contas do sistema"""

    def __init__(self) -> None:
        self._contas: dict[int, Conta] = {}
        self._proximo_numero: int = 1

    def add(self, titular: Cliente) -> Conta:
        numero = self._proximo_numero
        self._proximo_numero += 1

        nova_conta = Conta(titular, numero)
        self._contas[numero] = nova_conta
        titular.adicionar_conta(nova_conta)
        return nova_conta

    def get(self, numero: int) -> Conta | None:
        return self._contas.get(numero)

    def delete(self, numero: int) -> bool:
        if numero in self._contas:
            conta = self._contas.pop(numero)
            conta.titular.remover_conta(conta)
            return True
        return False

    def contas_do_cliente(self, cpf: str) -> list[Conta]:
        """Retorna todas as contas pertencentes ao CPF informado."""
        return [c for c in self._contas.values() if c.titular.cpf == cpf]

    def list(self) -> list[Conta]:
        """Retorna uma cópia da lista de contas"""
        return list(self._contas.values())

    def __len__(self) -> int:
        return len(self._contas)

    def __iter__(self):
        return iter(self._contas.values())


class HistoricoMovimentacoes(list):
    def adicionar(self, mov: Movimentacao) -> None:
        self.append(mov)

    def imprimir_extrato(self, saldo_atual: Decimal | None = None) -> None:
        print(f"{'Data/Hora':<20} | {'Operação':<32} | {'Tipo':<7} | {'Valor':>13} | {'Saldo Acumulado':>15}")
        print("-" * 96)
        saldo_acumulado = Decimal("0.00")
        for m in self:
            v = Decimal(str(m.valor))
            direcao = getattr(m, "direcao", "Crédito" if m.tipo == "Depósito" else "Débito")
            if direcao == "Crédito":
                saldo_acumulado += v
            else:
                saldo_acumulado -= v

            sinal = "+" if direcao == "Crédito" else "-"
            print(
                f"{m.data_hora:<20} | {m.tipo:<32} | {direcao:<7} | "
                f"{sinal}R$ {m.valor:>10.2f} | R$ {float(saldo_acumulado):>12.2f}"
            )
        print("-" * 96)
        saldo_final = saldo_atual if saldo_atual is not None else saldo_acumulado
        print(f"{'Saldo atual disponível:':<64} R$ {float(saldo_final):>12.2f}\n")
