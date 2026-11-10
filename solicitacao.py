"""Solicitações de abertura de conta feitas pelo cliente e analisadas pelo gerente."""
from datetime import datetime

from cliente import Cliente
from conta import Conta


class Status:
    """Classe simples para encapsular as constantes"""

    PENDENTE = "PENDENTE"
    APROVADA = "APROVADA"
    REJEITADA = "REJEITADA"
    INEXISTENTE = "INEXISTENTE"


class Solicitacao:
    def __init__(self, id: int, cliente: Cliente):
        self.id = id
        self.cliente = cliente          # já validado e com a senha em hash
        self.dataSolicitacao = datetime.now()
        self.status = Status.PENDENTE
        self.motivoRejeicao = ""

    def __repr__(self) -> str:
        return (f"ID: [{self.id}]\n"
                f"Cliente: {self.cliente.nome} ({self.cliente.cpf})\n"
                f"Data: {self.dataSolicitacao:%d/%m/%Y %H:%M}")

    def aprovar(self) -> None:
        """Aprova o pedido, alterando o status da solicitação"""
        self.status = Status.APROVADA

    def rejeitar(self, motivo: str) -> None:
        self.status = Status.REJEITADA
        self.motivoRejeicao = motivo


class Solicitacoes:
    """ Classe para controle de todas as solicitações do sistema"""

    def __init__(self) -> None:
        self._solicitacoes: dict[Cliente, Solicitacao] = {}
        self._proximo_id: int = 1

    def add(self, solicitante: Cliente) -> None:
        self._solicitacoes[solicitante] = Solicitacao(self._proximo_id, solicitante)
        self._proximo_id += 1

    def get(self, solicitante: Cliente) -> Solicitacao | None:
        return self._solicitacoes.get(solicitante)

    def delete(self, solicitante: Cliente) -> bool:
        if solicitante in self._solicitacoes:
            del self._solicitacoes[solicitante]
            return True
        return False

    def list(self) -> list[Solicitacao]: 
        """Retorna uma cópia da lista de solicitações"""
        return list(self._solicitacoes.values())

    def __len__(self) -> int:
        return len(self._solicitacoes)

    def __iter__(self):
        return iter(self._solicitacoes.values())


def ultima_solicitacao(cpf: str,
                       solicitacoes: dict[int, Solicitacao]) -> Solicitacao | None:
    do_cpf = [s for s in solicitacoes.values() if s.cliente.cpf == cpf]
    return max(do_cpf, key=lambda s: s.id, default=None)