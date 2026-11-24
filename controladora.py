from __future__ import annotations
from decimal import Decimal
from cliente import Cliente
from conta import Conta
from solicitacao import Solicitacao, Status
from persistencia import Banco


class BancoControlador:
    """Classe controladora central do banco (Camada de Serviço / Fachada de Aplicação)."""

    def __init__(self, banco: Banco) -> None:
        if hasattr(banco, "carregar_sistema"):
            self.banco = banco.carregar_sistema()
        else:
            self.banco = banco

    def cadastrar_cliente(self, cliente: Cliente) -> None:
        """Registra o cliente na coleção e persiste o estado em disco."""
        self.banco.clientes.add(cliente)
        self.banco.salvar_sistema()

    def autenticar_cliente(self, cpf: str, senha: str) -> Cliente | None:
        """Devolve o cliente se CPF e senha conferem; senão None."""
        cliente = self.banco.clientes.get(cpf)
        if cliente is not None and cliente.verificar_senha(senha):
            return cliente
        return None

    def obter_cliente(self, cpf: str) -> Cliente | None:
        """Obtém o cliente pelo CPF se ele existir."""
        return self.banco.clientes.get(cpf)

    def cadastrar_conta(self, cliente: Cliente) -> Conta:
        """Cria e associa uma nova conta ao cliente e persiste em disco."""
        conta = self.banco.contas.add(titular=cliente)
        self.banco.salvar_sistema()
        return conta

    def solicitar_abertura_conta(self, cliente: Cliente) -> Solicitacao:
        """Cria uma nova solicitação se não houver outra pendente para o cliente."""
        solicitacao_existente = self.banco.solicitacoes.get(cliente.cpf)
        if solicitacao_existente is not None and solicitacao_existente.status == Status.PENDENTE:
            raise ValueError("Já existe uma solicitação pendente para essa conta.")

        solicitacao = self.banco.solicitacoes.add(solicitante=cliente)
        self.banco.salvar_sistema()
        return solicitacao

    def acompanhar_solicitacao(self, cliente: Cliente) -> Solicitacao | None:
        """Recupera a solicitação associada ao cliente."""
        return self.banco.solicitacoes.get(cliente.cpf)

    def aprovar_solicitacao(self, solicitacao: Solicitacao) -> Conta:
        """Aprova a solicitação, cria a conta vinculada e persiste em disco."""
        solicitacao.aprovar()
        # Busca o cliente da base para vincular a conta na mesma referência
        cliente = self.banco.clientes.get(solicitacao.cliente.cpf) or solicitacao.cliente
        conta = self.banco.contas.add(titular=cliente)
        self.banco.salvar_sistema()
        return conta

    def rejeitar_solicitacao(
        self, solicitacao: Solicitacao, motivo: str = "(Não informado)"
    ) -> None:
        """Rejeita a solicitação informando a justificativa e persiste em disco."""
        solicitacao.rejeitar(motivo)
        self.banco.salvar_sistema()

    def listar_solicitacoes_pendentes(self) -> list[Solicitacao]:
        """Lista todas as solicitações com status PENDENTE."""
        return [s for s in self.banco.solicitacoes.list() if s.status == Status.PENDENTE]

    def obter_contas_cliente(self, cliente: Cliente) -> list[Conta]:
        """Retorna todas as contas pertencentes ao cliente."""
        return self.banco.contas.contas_do_cliente(cliente.cpf)

    def obter_conta(self, numero: int) -> Conta | None:
        """Busca uma conta pelo seu número."""
        return self.banco.contas.get(numero)

    def realizar_deposito(self, conta: Conta, valor: float) -> None:
        """Realiza depósito na conta e persiste imediatamente."""
        conta.depositar(valor)
        self.banco.salvar_sistema()

    def realizar_saque(self, conta: Conta, valor: float) -> None:
        """Realiza saque na conta com validação de saldo e persiste."""
        conta.sacar(valor)
        self.banco.salvar_sistema()

    def realizar_transferencia(
        self,
        pagador: Conta,
        recebedor: Conta,
        valor: float,
        modalidade: str = "Transferência",
    ) -> None:
        """Realiza transferência coordenada entre pagador e recebedor e persiste."""
        pagador.transferir(recebedor, valor, modalidade=modalidade)
        self.banco.salvar_sistema()

    # Aliases de compatibilidade
    def RealizarTransferencia(
        self, pagador: Conta, recebedor: Conta, valor: float, modalidade: str = "Transferência"
    ) -> None:
        self.realizar_transferencia(pagador, recebedor, valor, modalidade=modalidade)

    def remover_cliente(self, cpf: str) -> None:
        """Remove o cliente e suas contas, garantindo que não haja saldo positivo."""
        cliente = self.banco.clientes.get(cpf)
        if cliente is None:
            raise ValueError("Não há cliente cadastrado com o CPF informado")

        contas = self.banco.contas.contas_do_cliente(cpf)
        saldo_total = sum(c.saldo for c in contas)
        if saldo_total > Decimal("0.00"):
            raise ValueError(
                f"Não é possível remover o cliente. Existe saldo positivo de R$ {float(saldo_total):.2f} "
                "em suas contas. Realize o saque de todos os valores antes de efetuar a exclusão."
            )

        for conta in contas:
            self.banco.contas.delete(conta.numeroConta)

        self.banco.solicitacoes.delete(cpf)
        self.banco.clientes.delete(cpf)
        self.banco.salvar_sistema()


# Instância controladora singleton para compatibilidade com o projeto
control = BancoControlador(Banco())
