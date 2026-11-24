import re
from getpass import getpass
from cliente import Cliente
from conta import Conta
from controladora import BancoControlador, control
from solicitacao import Solicitacao, Status
from entrada import (
    ler_dados_cliente,
    ler_cpf_senha,
    ler_cpf_cliente,
    ler_opcao,
    ler_valor,
)


class Cli:
    def __init__(self, controlador: BancoControlador):
        """Esse objeto recebe uma instância da classe controladora para interagir com o sistema."""
        self.ctrl = controlador

    # =========================================================================
    # INTERFACES PÚBLICAS
    # =========================================================================

    def interface_login(self) -> None:
        """Portal de entrada do Cliente (Login ou Novo Cadastro)."""
        while True:
            self._print_menu_login()
            match ler_opcao():
                case 1:
                    cpf, senha = ler_cpf_senha()
                    cliente = self.ctrl.autenticar_cliente(cpf, senha)
                    if cliente is None:
                        print("\nCPF ou senha inválidos.")
                        continue

                    print(f"\nBem-vindo(a), {cliente.nome}!")
                    self.interface_cliente(cliente)
                case 2:
                    try:
                        cliente = ler_dados_cliente()
                        self.ctrl.cadastrar_cliente(cliente)
                        print("\nCadastro realizado com sucesso!")
                        self.interface_cliente(cliente)
                    except ValueError as erro:
                        print(f"\nErro no cadastro: {erro}")
                case 0:
                    break
                case _:
                    print("\nOpção inválida.")

    def interface_cliente(self, cliente: Cliente) -> None:
        """Gerencia o menu do cliente logado, direcionando para operações de conta se ativa."""
        while True:
            # Sincroniza referência de contas do cliente
            contas = self.ctrl.obter_contas_cliente(cliente)
            if not contas:
                sair = self._menu_cliente_sem_conta(cliente)
                if sair:
                    break
            else:
                self._menu_cliente_com_conta(cliente, contas)
                break

    def interface_gerente(self) -> None:
        """Portal Administrativo da Gerência."""
        # Proteção administrativa simples
        senha = getpass("\nInforme a senha de administrador: ")
        if senha != "admin123":
            print("Acesso negado! Senha administrativa incorreta.")
            return

        while True:
            self._print_menu_gerente()
            match ler_opcao():
                case 1:
                    print("\n--- Cadastro de Cliente ---")
                    try:
                        cliente = ler_dados_cliente()
                        self.ctrl.cadastrar_cliente(cliente)
                        print(f"\nCliente {cliente.nome} cadastrado com sucesso!")
                    except ValueError as erro:
                        print(f"\nErro no cadastro: {erro}")

                case 2:
                    print("\n--- Abertura de Conta ---")
                    cpf = ler_cpf_cliente("\tInforme o CPF do cliente: ")
                    cliente = self.ctrl.obter_cliente(cpf)
                    if cliente is None:
                        print("\nCliente não encontrado.")
                        continue
                    try:
                        conta = self.ctrl.cadastrar_conta(cliente)
                        print(f"\nConta nº {conta.numeroConta} aberta e vinculada ao cliente {cliente.nome}.")
                    except ValueError as erro:
                        print(f"\nErro na abertura de conta: {erro}")

                case 3:
                    print("\n--- Remoção Segura de Cliente ---")
                    cpf = ler_cpf_cliente("\tInforme o CPF do cliente: ")
                    try:
                        confirm = input(f"\tConfirma a remoção do cliente de CPF {cpf}? [S/N]: ").strip().lower()
                        if confirm == "s":
                            self.ctrl.remover_cliente(cpf)
                            print("\nCliente e suas contas foram removidos com sucesso.")
                        else:
                            print("\nOperação cancelada.")
                    except ValueError as erro:
                        print(f"\nErro: {erro}")

                case 4:
                    pendentes = self.ctrl.listar_solicitacoes_pendentes()
                    if not pendentes:
                        print("\nNenhuma solicitação pendente no momento.")
                        continue

                    print(f"\n=== Solicitações Pendentes ({len(pendentes)}) ===")
                    for solicitacao in pendentes:
                        voltar = self._menu_analisar_solicitacao(solicitacao)
                        if voltar:
                            break

                case 5:
                    self._listar_todos_clientes_e_contas()

                case 0:
                    print("\nSaindo do Portal da Gerência...")
                    break
                case _:
                    print("\nOpção inválida.")

    # =========================================================================
    # MENUS AUXILIARES
    # =========================================================================

    def _menu_cliente_sem_conta(self, cliente: Cliente) -> bool:
        """Menu para cliente que ainda não possui conta bancária aprovada."""
        while True:
            print("\n=== BANCO 24 HORAS - PORTAL DO CLIENTE ===")
            print(f"Usuário: {cliente.nome} (Sem conta ativa)")
            print("1. Solicitar abertura de conta")
            print("2. Acompanhar minhas solicitações")
            print("0. Desconectar")
            print("> ", end="")

            match ler_opcao():
                case 1:
                    try:
                        sol = self.ctrl.solicitar_abertura_conta(cliente)
                        print(f"\nSolicitação nº {sol.id} enviada com sucesso! Aguarde a análise da gerência.")
                    except ValueError as erro:
                        print(f"\nAviso: {erro}")
                case 2:
                    solicitacao = self.ctrl.acompanhar_solicitacao(cliente)
                    self._print_status_solicitacao(solicitacao)
                case 0:
                    return True
                case _:
                    print("\nOpção inválida.")

    def _menu_cliente_com_conta(self, cliente: Cliente, contas: list[Conta]) -> None:
        """Menu transacional completo para cliente com conta ativa."""
        if len(contas) == 1:
            conta_ativa = contas[0]
        else:
            print("\nVocê possui mais de uma conta. Selecione qual deseja acessar:")
            for idx, c in enumerate(contas, 1):
                print(f"[{idx}] Conta nº {c.numeroConta} - Saldo: R$ {float(c.saldo):.2f}")
            print("[0] Desconectar")
            print("> ", end="")
            op = ler_opcao()
            if op is None or op == 0 or op > len(contas):
                return
            conta_ativa = contas[op - 1]

        while True:
            print(f"\n=== SESSÃO BANCÁRIA - CONTA Nº {conta_ativa.numeroConta} ===")
            print(f"Titular: {cliente.nome} | Saldo: R$ {float(conta_ativa.saldo):.2f}")
            print("-" * 50)
            print("1. Consultar Extrato Completo")
            print("2. Realizar Depósito")
            print("3. Realizar Saque")
            print("4. Realizar Transferência")
            print("5. Solicitar Nova Conta / Acompanhar Solicitações")
            print("0. Desconectar (Logout)")
            print("> ", end="")

            match ler_opcao():
                case 1:
                    conta_ativa.extrato()

                case 2:
                    try:
                        valor = ler_valor("\tInforme o valor a depositar (R$): ")
                        self.ctrl.realizar_deposito(conta_ativa, valor)
                        print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!")
                    except ValueError as erro:
                        print(f"\nErro no depósito: {erro}")

                case 3:
                    try:
                        valor = ler_valor("\tInforme o valor a sacar (R$): ")
                        self.ctrl.realizar_saque(conta_ativa, valor)
                        print(f"\nSaque de R$ {valor:.2f} concluído com sucesso!")
                    except ValueError as erro:
                        print(f"\nErro no saque: {erro}")

                case 4:
                    try:
                        entrada_conta = input("\tInforme o número da conta de destino: ").strip()
                        if not entrada_conta.isdigit():
                            print("\nNúmero de conta inválido.")
                            continue
                        num_dest = int(entrada_conta)
                        destino = self.ctrl.obter_conta(num_dest)
                        if destino is None:
                            print("\nConta de destino não encontrada.")
                            continue

                        valor = ler_valor(f"\tValor a transferir para {destino.titular.nome} (R$): ")
                        self.ctrl.realizar_transferencia(conta_ativa, destino, valor)
                        print(f"\nTransferência de R$ {valor:.2f} realizada com sucesso para Conta {destino.numeroConta} ({destino.titular.nome})!")
                    except ValueError as erro:
                        print(f"\nErro na transferência: {erro}")

                case 5:
                    self._menu_cliente_sem_conta(cliente)

                case 0:
                    print("\nSessão encerrada com sucesso.")
                    break
                case _:
                    print("\nOpção inválida.")

    def _listar_todos_clientes_e_contas(self) -> None:
        """Lista resumo de todos os clientes e contas persistidos."""
        clientes = self.ctrl.banco.clientes.list()
        if not clientes:
            print("\nNenhum cliente cadastrado no sistema.")
            return

        print("\n" + "=" * 65)
        print("          RELATÓRIO GERAL DE CLIENTES E CONTAS ATIVAS")
        print("=" * 65)
        for c in clientes:
            contas = self.ctrl.obter_contas_cliente(c)
            desc_contas = (
                ", ".join([f"Conta {cta.numeroConta} (R$ {float(cta.saldo):.2f})" for cta in contas])
                if contas
                else "(Sem contas ativas)"
            )
            print(f"• {c.nome} | CPF: {c.cpf} | Tel: {c.telefone} | Email: {c.email}")
            print(f"  Contas: {desc_contas}")
        print("=" * 65 + "\n")

    def _menu_analisar_solicitacao(self, solicitacao: Solicitacao) -> bool:
        """Apresenta opções para aprovar ou rejeitar uma solicitação."""
        print("\n" + "-" * 50)
        print(solicitacao)
        print("-" * 50)
        acao = input("[A]provar, [R]ejeitar ou [V]oltar: ").strip().lower()
        match acao:
            case "a":
                conta = self.ctrl.aprovar_solicitacao(solicitacao)
                print(f"\nSolicitação APROVADA! Conta nº {conta.numeroConta} criada para {solicitacao.cliente.nome}.")
                return False
            case "r":
                motivo = input("\tMotivo da rejeição (opcional): ").strip()
                if motivo:
                    self.ctrl.rejeitar_solicitacao(solicitacao, motivo)
                else:
                    self.ctrl.rejeitar_solicitacao(solicitacao)
                print("\nSolicitação REJEITADA.")
                return False
            case "v":
                return True
            case _:
                print("\nOpção inválida.")
                return False

    def _print_status_solicitacao(self, solicitacao: Solicitacao | None) -> None:
        if solicitacao is None:
            print("\nNenhuma solicitação encontrada para o seu usuário.")
            return

        print("\n" + "-" * 40)
        match solicitacao.status:
            case Status.PENDENTE:
                print(f"Solicitação nº {solicitacao.id}: Ainda está EM ANÁLISE pela gerência.")
            case Status.APROVADA:
                print(f"Solicitação nº {solicitacao.id}: Foi APROVADA! Sua conta já está liberada.")
            case Status.REJEITADA:
                print(f"Solicitação nº {solicitacao.id}: Foi REJEITADA.")
                if solicitacao.motivoRejeicao:
                    print(f"Motivo: {solicitacao.motivoRejeicao}")
        print("-" * 40)

    def _print_menu_login(self) -> None:
        print("\n=== LOGIN - BANCO 24 HORAS ===\n"
              "1. Fazer Login\n"
              "2. Fazer Cadastro\n"
              "0. Voltar / Sair\n"
              "> ", end="")

    def _print_menu_gerente(self) -> None:
        print("\n=== PORTAL DA GERÊNCIA ===\n"
              "1. Cadastrar Cliente\n"
              "2. Abrir Conta\n"
              "3. Remover Cliente (com trava de segurança)\n"
              "4. Analisar Solicitações Pendentes\n"
              "5. Listar Todos os Clientes e Contas\n"
              "0. Sair\n"
              "> ", end="")


# Objeto global a ser utilizado nos pontos de entrada
cli = Cli(control)
