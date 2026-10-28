import re
from cliente import Cliente, autenticar
from conta import Conta
from serializacao import carregar_dados, salvar_dados
from controladora import BancoControlador, control
from getpass import getpass
import solicitacao as Solicitacao
from solicitacao import SolicitacaoConta, listar_pendentes

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
                        # 
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
                        # TODO: implementar função abaixo
                        # self.ctrl.cadastrar_cliente(cliente)
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
                        print("Solicitação Enviada.")
                        self.ctrl.solicitar_abertura_conta(cliente)
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
                    # Como ainda não temos uma base de dados, será necessário 
                    # instanciar um novo cliente aqui para cadastrar a conta'
                    cliente = self._ler_dados_cliente()
                    self.ctrl.cadastrar_conta(cliente)
                case 2:
                    print("...")  # TODO: remover cliente
                case 3:
                    # TODO: é ideal trocar a função de analisar solicitações por 
                    # uma que retorne as solucitões como uma lista para serem 
                    # impressas aqui
                    self.ctrl.analisar_solicitacoes()
                case 0:
                    break
                case _:
                    print("Opção inválida.")


    """" Os métodos abaixo são auxiliares privados e não devem 
    ser chamados em outros locais do sistema"""

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
        # TODO: delegar carregamento de dados para controler
        _, _, solicitacoes = carregar_dados()
        pendentes = len(listar_pendentes(solicitacoes))
        print("\n1. Cadastrar Cliente e Criar Conta\n"
            "2. Remover Cliente\n"
            f"3. Solicitações de abertura de conta ({pendentes} pendente(s))\n"
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

    def _print_status_solicitacao(self, solicitacao : SolicitacaoConta | None) -> None:
        if solicitacao is None:
            print("Solicitação não encontrada")
            return

        match solicitacao.status:
            case Solicitacao.PENDENTE:
                print("Sua solicitação ainda está em análise.")
            case Solicitacao.APROVADA:
                print("Sua solicitação foi APROVADA! Já pode utilizar a conta.")
            case Solicitacao.REJEITADA:
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



# Objeto global a ser utilizado
cli = Cli(control)