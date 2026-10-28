from interface import cli
from cliente import Cliente, autenticar
from serializacao import carregar_dados, salvar_dados
from solicitacao import *

class BancoControlador:
    def acompanhar_solicitacao(self, cliente: Cliente) -> SolicitacaoConta | None:
        _, _, solicitacoes = carregar_dados()
        return ultima_solicitacao(cliente.cpf, solicitacoes)


    def cadastrar_cliente_e_criar_conta(
        self,
        cliente: Cliente,
        clientes: dict[str, Cliente],
        contas: dict[int, Conta],
    ) -> Conta:
        """Registra o cliente e abre a conta dele. Lança ValueError se o CPF já existir."""
        if cliente.cpf in clientes:
            raise ValueError("Já existe um cliente cadastrado com este CPF.")

        conta = Conta(cliente)
        clientes[cliente.cpf] = cliente
        contas[conta.numeroConta] = conta
        return conta


    def cadastrar_conta(self, cliente: Cliente) -> None:
        try:
            #TODO: implementar lógica de adição da nova conta ao dicionário global
            conta = Conta(cliente)
        except ValueError as erro:
            print(f"Cadastro não realizado: {erro}")
            return

        # salvar_dados(clientes, contas, solicitacoes)
        print(f"Conta criada:")
        print(conta)


    def analisar_solicitacoes(self) -> None:
        while True:
            clientes, contas, solicitacoes = carregar_dados()
            pendentes: list[SolicitacaoConta] = listar_pendentes(solicitacoes)
            if not pendentes:
                print("Nenhuma solicitação pendente.")
                return

            print("\nSolicitações pendentes:")
            for solicitacao in pendentes:
                cliente = solicitacao.cliente
                print(f"  [{solicitacao.id}] {cliente.nome} | CPF {cliente.cpf} | "
                      f"{cliente.email} | tel {cliente.telefone} | "
                      f"{solicitacao.dataSolicitacao:%d/%m/%Y %H:%M}")

            try:
                escolhido = int(input("Nº da solicitação para analisar (0 para voltar): "))
            except ValueError:
                print("Opção inválida.")
                continue
            if escolhido == 0:
                return
            if escolhido not in {solicitacao.id for solicitacao in pendentes}:
                print("Solicitação não encontrada.")
                continue

            acao = input("[A]provar, [R]ejeitar ou [V]oltar: ").strip().lower()
            try:
                if acao == "a":
                    conta = aprovar(escolhido, clientes, contas, solicitacoes)
                    salvar_dados(clientes, contas, solicitacoes)
                    print(f"Aprovada! Conta nº {conta.numeroConta} criada.")
                elif acao == "r":
                    motivo = input("Motivo da rejeição (opcional): ")
                    rejeitar(escolhido, solicitacoes, motivo)
                    salvar_dados(clientes, contas, solicitacoes)
                    print("Solicitação rejeitada.")
            except ValueError as erro:
                print(f"Não foi possível concluir: {erro}")

    def autenticar_cliente(self, cpf: str, senha: str) -> None:
        clientes, _ , _ = carregar_dados()
        cliente = autenticar(cpf, senha, clientes)
        if cliente is None:
            print("CPF ou senha inválidos.")
            return

    def solicitar_abertura_conta(self, cliente: Cliente) -> None:
        try:
            clientes, contas, solicitacoes = carregar_dados()
            solicitacao = solicitar_conta(cliente, clientes, solicitacoes)
        except ValueError as erro:
            print(f"Solicitação não enviada: {erro}")
            return

        salvar_dados(clientes, contas, solicitacoes)
        print(f"\nSolicitação nº {solicitacao.id} enviada! Aguarde a análise do gerente.")
        print("Use a opção 2 do menu para acompanhar.")


control = BancoControlador()