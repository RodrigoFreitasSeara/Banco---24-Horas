"""Solicitações de abertura de conta feitas pelo cliente e analisadas pelo gerente."""
from datetime import datetime

from cliente import Cliente
from conta import Conta

PENDENTE = "PENDENTE"
APROVADA = "APROVADA"
REJEITADA = "REJEITADA"
INEXISTENTE = "INEXISTENTE"


class SolicitacaoConta:
    def __init__(self, id: int, cliente: Cliente):
        self.id = id
        self.cliente = cliente          # já validado e com a senha em hash
        self.dataSolicitacao = datetime.now()
        self.status = PENDENTE
        self.motivoRejeicao = ""

    def __repr__(self) -> str:
        return (f"SolicitacaoConta(id={self.id!r}, cpf={self.cliente.cpf!r}, "
                f"status={self.status!r})")


def solicitar_conta(cliente: Cliente,
                    clientes: dict[str, Cliente],
                    solicitacoes: dict[int, SolicitacaoConta]) -> SolicitacaoConta:
    """Registra um pedido PENDENTE. Lança ValueError se o CPF já for cliente ou já tiver pedido em análise."""
    if cliente.cpf in clientes:
        raise ValueError("Este CPF já possui cadastro. Use a opção Entrar.")
    if any(s.cliente.cpf == cliente.cpf and s.status == PENDENTE
           for s in solicitacoes.values()):
        raise ValueError("Já existe uma solicitação em análise para este CPF.")

    novo_id = max(solicitacoes, default=0) + 1
    solicitacao = SolicitacaoConta(novo_id, cliente)
    solicitacoes[novo_id] = solicitacao
    return solicitacao


def listar_pendentes(solicitacoes: dict[int, SolicitacaoConta]) -> list[SolicitacaoConta]:
    return [s for s in solicitacoes.values() if s.status == PENDENTE]


def _buscar_pendente(solicitacao_id: int,
                     solicitacoes: dict[int, SolicitacaoConta]) -> SolicitacaoConta:
    solicitacao = solicitacoes.get(solicitacao_id)
    if solicitacao is None or solicitacao.status != PENDENTE:
        raise ValueError("Solicitação não encontrada ou já analisada.")
    return solicitacao


def aprovar(solicitacao_id: int,
            clientes: dict[str, Cliente],
            contas: dict[int, Conta],
            solicitacoes: dict[int, SolicitacaoConta]) -> Conta:
    """Aprova o pedido: cadastra o cliente e cria a conta dele."""
    solicitacao = _buscar_pendente(solicitacao_id, solicitacoes)
    cliente = solicitacao.cliente
    if cliente.cpf in clientes:
        raise ValueError("Este CPF já foi cadastrado por outro caminho. Rejeite a solicitação.")

    conta = Conta(cliente)
    clientes[cliente.cpf] = cliente
    contas[conta.numeroConta] = conta
    solicitacao.status = APROVADA
    return conta


def rejeitar(solicitacao_id: int,
             solicitacoes: dict[int, SolicitacaoConta],
             motivo: str = "") -> None:
    solicitacao = _buscar_pendente(solicitacao_id, solicitacoes)
    solicitacao.status = REJEITADA
    solicitacao.motivoRejeicao = motivo.strip()


def ultima_solicitacao(cpf: str,
                       solicitacoes: dict[int, SolicitacaoConta]) -> SolicitacaoConta | None:
    do_cpf = [s for s in solicitacoes.values() if s.cliente.cpf == cpf]
    return max(do_cpf, key=lambda s: s.id, default=None)