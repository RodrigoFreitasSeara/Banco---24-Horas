from interface import cli
from cliente import Cliente
from solicitacao import Solicitacao, Status
from persistencia import Banco

# TODO: implementar salvamento dos dados em diferentes momentos
class BancoControlador:
    """Classe controladora"""

    def __init__(self, banco: Banco) -> None:
        self.banco = banco.carregar_sistema()

    def acompanhar_solicitacao(self, cliente: Cliente) -> Solicitacao | None:
        return self.banco.solicitacoes.get(solicitante=cliente)

    def cadastrar_cliente(self, cliente: Cliente) -> None:
        """Registra o cliente. Lança ValueError se o CPF já existir."""
        self.banco.clientes.add(cliente)


    def cadastrar_conta(self, cliente: Cliente) -> None:
        self.banco.contas.add(titular=cliente)


    def autenticar_cliente(self, cpf: str, senha: str) -> Cliente | None:
        """Devolve o cliente se CPF e senha conferem; senão None (sem dizer qual dos dois errou)."""

        cliente = self.banco.clientes.get(cpf)
        if cliente is not None and cliente.verificar_senha(senha):
            return cliente
        return None

    def obter_cliente(self, cpf: str) -> Cliente | None:
        """Pula a autenticação e obtém o cliente pelo CPF se ele existir"""

        return self.banco.clientes.get(cpf)


    def remover_cliente(self, cpf: str) -> None:
        """Remove um cliente do sistema juntamente com suas contas"""

        if not self.banco.clientes.delete(cpf):
            raise ValueError("Não há cliente cadastrado com o CPF informado")
        # TODO: implementar em clientes uma lista de contas que ele pertence
        # para viabilizar a remoção das contas

    def solicitar_abertura_conta(self, cliente: Cliente) -> None:
        solicitacaoExistente = self.banco.solicitacoes.get(cliente)

        # Só será possível abrir uma nova solicitação se não houver outra pendente
        if solicitacaoExistente is not None and solicitacaoExistente.status is not Status.PENDENTE:
            self.banco.solicitacoes.add(solicitante=cliente)

        raise ValueError("Já existe uma solicitação pendente para essa conta")


    def aprovar_solicitacao(self, solicitacao: Solicitacao):
        solicitacao.aprovar()
        self.banco.contas.add(titular=solicitacao.cliente)

    def rejeitar_solicitacao(self, solicitacao: Solicitacao, motivo="(Não informado)"):
        solicitacao.rejeitar(motivo)

    def listar_solicitacoes_pendentes(self) -> list[Solicitacao]:
        return [s for s in self.banco.solicitacoes.list() if s.status == Status.PENDENTE]



control = BancoControlador(Banco())