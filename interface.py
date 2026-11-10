import re
from cliente import Cliente
from conta import Conta
from controladora import BancoControlador, control
from getpass import getpass
from solicitacao import Solicitacao, Status

class Cli:
    def __init__(self, controlador: BancoControlador):
        """ Esse objeto deve receber uma instância da classe 
        controladora para chamar as funções que interagem com 
        o sistema"""
        self.ctrl = controlador

    """" Os métodos abaixo são interfaces públicas e devem 
    ser chamados em outros locais do sistema"""

    def interface_login(self) -> None:
            while True:
                self._print_menu_login()
                match self._ler_opcao():
                    case 1:
                        """Pede as credenciais e chama o controlador para autenticar"""
                        cpf, senha = self._ler_cpf_senha()
                        cliente = self.ctrl.autenticar_cliente(cpf, senha)
                        if cliente is None:
                            print("CPF ou senha inválidos.")
                            continue

                        print(f"\nBem-vindo(a), {cliente.nome}!")
                        self.interface_cliente(cliente)
                    case 2:
                        cliente = self._ler_dados_cliente()
                        self.ctrl.cadastrar_cliente(cliente)
                        self.interface_cliente(cliente)
                    case 0:
                        break
                    case _:
                        print("Opção inválida.")

        
    def interface_cliente(self, cliente: Cliente) -> None:
            while True:
                self._print_menu_cliente()
                match self._ler_opcao():
                    case 1:
                        try:
                            self.ctrl.solicitar_abertura_conta(cliente)
                        except ValueError as erro:
                            print(erro)
                    case 2:
                        solicitacao = self.ctrl.acompanhar_solicitacao(cliente)
                        self._print_status_solicitacao(solicitacao)
                    case 0:
                        break
                    case _:
                        print("Opção inválida.")


    def interface_gerente(self) -> None:
        while True:
            self._print_menu_gerente()
            match self._ler_opcao():
                case 1:
                    cpf = self._ler_cpf_cliente()
                    cliente = self.ctrl.obter_cliente(cpf)

                    if cliente is None:
                        print("Não há cliente cadastrado com o CPF informado")
                        continue

                    self.ctrl.cadastrar_conta(cliente)
                case 2:
                    cpf = self._ler_cpf_cliente()

                    try:
                        self.ctrl.remover_cliente(cpf)
                    except ValueError as erro:
                        print(erro)
                case 3:
                    pendentes = self.ctrl.listar_solicitacoes_pendentes()
                    if not pendentes:
                        print("Nenhuma solicitação pendente.")
                        continue

                    print("\nSolicitações pendentes:")
                    for solicitacao in pendentes:
                        self._menu_analisar_solicitacao(solicitacao)
                case 4:
                    print("...") # TODO: implementar criação instantânea de conta pelo gerente
                case 0:
                    break
                case _:
                    print("Opção inválida.")


    """" Os métodos abaixo são auxiliares privados e não devem 
    ser chamados em outros locais do sistema"""

    def _ler_cpf_cliente(self) -> str:
        cpf = re.sub(r"\D", "", input("\tInforme o CPF do cliente: "))
        return cpf

    def _ler_cpf_senha(self) -> tuple[str, str]:
        cpf = re.sub(r"\D", "", input("\tCPF: "))
        senha = getpass("\tSenha: ")
        return cpf, senha

    def _login_cliente(self) -> Cliente:
        """Pede as credenciais e chama o controlador para autenticar"""
        cpf, senha = self._ler_cpf_senha()
        resultado = self.ctrl.autenticar_cliente(cpf, senha)

        if resultado is None:
            raise ValueError("CPF ou senha inválidos.")

        return resultado

    def _print_menu_cliente(self) -> None:
        print("\n=== BANCO 24 HORAS ===\n"
            "1. Solicitar abertura de conta\n"
            "2. Acompanhar minhas solicitações\n"
            "0. Sair\n"
            "> ", end=""
        )

    def _print_menu_gerente(self) -> None:
        print("\n1. Cadastrar Cliente\n"
            "2. Remover Cliente\n"
            "3. Analisar Solicitações de Abertura de Contas\n"
            "4. Abrir Conta para Cliente\n"
            "0. Sair\n"
            "> ", end=""
        )

    def _print_menu_login(self) -> None:
        print("\n=== LOGIN ===\n"
            "1. Fazer Login\n"
            "2. Fazer Cadastro\n"
            "> ", end=""    
        )

    def _ler_opcao(self) -> int | None:
        try:
            return int(input())
        except ValueError:
            return None

    def _print_status_solicitacao(self, solicitacao : Solicitacao | None) -> None:
        if solicitacao is None:
            print("Solicitação não encontrada")
            return

        match solicitacao.status:
            case Status.PENDENTE:
                print("Sua solicitação ainda está em análise.")
            case Status.APROVADA:
                print("Sua solicitação foi APROVADA! Já pode utilizar a conta.")
            case Status.REJEITADA:
                print("Sua solicitação foi REJEITADA.")
                if solicitacao.motivoRejeicao:
                    print(f"Motivo: {solicitacao.motivoRejeicao}")

    def _ler_dados_cliente(self) -> Cliente:
        """Pede os dados do cadastro. Lança ValueError se algum for inválido."""
        print("Informe os seguintes dados:")
        nome = input("\tNome: ")
        cpf = input("\tCPF: ")
        telefone = input("\tTelefone (com DDD): ")
        email = input("\tE-mail: ")
        senha = getpass("\tSenha (mín. 5 caracteres): ")
        confirmacao = getpass("\tConfirme a senha: ")

        if senha != confirmacao:
            raise ValueError("As senhas não conferem.")

        return Cliente(nome, cpf, telefone, email, senha)

    def _menu_analisar_solicitacao(self, solicitacao: Solicitacao) -> None:
            print(solicitacao)

            acao = input("[A]provar, [R]ejeitar ou [V]oltar: ").strip().lower()
            match acao:
                case "a":
                    self.ctrl.aprovar_solicitacao(solicitacao)
                    print("Solcitação Aprovada!")
                case "r":
                    motivo = input("Motivo da rejeição (opcional): ")
                    if motivo:
                        self.ctrl.rejeitar_solicitacao(solicitacao, motivo)
                    else:
                        self.ctrl.rejeitar_solicitacao(solicitacao)

                    print("Solicitação rejeitada.")
                case "v":
                    return
                case _:
                    print("Opção Inválida.")



# Objeto global a ser utilizado
cli = Cli(control)