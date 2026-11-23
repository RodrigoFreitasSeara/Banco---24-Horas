"""Solicitações de abertura de conta feitas pelo cliente e analisadas pelo gerente."""
from datetime import datetime
from cliente import Cliente


class Status:
    """Constantes para o ciclo de vida da solicitação"""

    PENDENTE = "PENDENTE"
    APROVADA = "APROVADA"
    REJEITADA = "REJEITADA"
    INEXISTENTE = "INEXISTENTE"


class Solicitacao:
    def __init__(self, id: int, cliente: Cliente):
        self.id = id
        self.cliente = cliente
        self.dataSolicitacao = datetime.now()
        self.status = Status.PENDENTE
        self.motivoRejeicao = ""

    def __repr__(self) -> str:
        motivo = f"\nMotivo da Rejeição: {self.motivoRejeicao}" if self.motivoRejeicao else ""
        return (
            f"Solicitação ID: [{self.id}]\n"
            f"Cliente: {self.cliente.nome} (CPF: {self.cliente.cpf})\n"
            f"Status: {self.status}\n"
            f"Data: {self.dataSolicitacao:%d/%m/%Y %H:%M}{motivo}"
        )

    def aprovar(self) -> None:
        """Aprova o pedido, alterando o status da solicitação"""
        self.status = Status.APROVADA

    def rejeitar(self, motivo: str) -> None:
        """Rejeita o pedido registrando a justificativa"""
        self.status = Status.REJEITADA
        self.motivoRejeicao = motivo


class Solicitacoes:
    """Classe para controle de todas as solicitações do sistema"""

    def __init__(self) -> None:
        self._solicitacoes: dict[str, Solicitacao] = {}
        self._proximo_id: int = 1

    def add(self, solicitante: Cliente) -> Solicitacao:
        solicitacao = Solicitacao(self._proximo_id, solicitante)
        self._solicitacoes[solicitante.cpf] = solicitacao
        self._proximo_id += 1
        return solicitacao

    def get(self, solicitante: Cliente | str) -> Solicitacao | None:
        cpf = solicitante.cpf if isinstance(solicitante, Cliente) else str(solicitante)
        return self._solicitacoes.get(cpf)

    def delete(self, solicitante: Cliente | str) -> bool:
        cpf = solicitante.cpf if isinstance(solicitante, Cliente) else str(solicitante)
        if cpf in self._solicitacoes:
            del self._solicitacoes[cpf]
            return True
        return False

    def list(self) -> list[Solicitacao]:
        """Retorna uma cópia da lista de solicitações"""
        return list(self._solicitacoes.values())

    def __len__(self) -> int:
        return len(self._solicitacoes)

    def __iter__(self):
        return iter(self._solicitacoes.values())
