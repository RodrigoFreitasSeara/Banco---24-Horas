from serializacao import *
import os.path
from cliente import autenticar
from entrada import ler_cpf_senha, ler_dados_cliente, ler_opcao
from solicitacao import APROVADA, PENDENTE, REJEITADA, solicitar_conta, ultima_solicitacao

arquivoClientes = "clientes.pkl" 
arquivoContas = "contas.pkl" 


def print_menu_inicial():
    print("\n=== BANCO 24 HORAS ===\n"
          "1. Entrar\n"
          "2. Solicitar abertura de conta\n"
          "3. Acompanhar minha solicitação\n"
          "0. Sair\n"
          "> ", end='')


def solicitar_abertura_de_conta():
    try:
        novoCliente = ler_dados_cliente()
        clientes, contas, solicitacoes = carregar_dados()
        solicitacao = solicitar_conta(novoCliente, clientes, solicitacoes)
    except ValueError as erro:
        print(f"Solicitação não enviada: {erro}")
        return

    salvar_dados(clientes, contas, solicitacoes)
    print(f"\nSolicitação nº {solicitacao.id} enviada! Aguarde a análise do gerente.")
    print("Use a opção 3 do menu para acompanhar.")


def acompanhar_solicitacao():
    cpf, senha = ler_cpf_senha()
    _, _, solicitacoes = carregar_dados()
    solicitacao = ultima_solicitacao(cpf, solicitacoes)

    # a senha é exigida para não revelar a ninguém o status de um CPF
    if solicitacao is None or not solicitacao.cliente.verificar_senha(senha):
        print("CPF ou senha inválidos.")
        return

    if solicitacao.status == PENDENTE:
        print("Sua solicitação está em análise.")
    elif solicitacao.status == APROVADA:
        print("Sua solicitação foi APROVADA! Já pode entrar no banco.")
    elif solicitacao.status == REJEITADA:
        print("Sua solicitação foi REJEITADA.")
        if solicitacao.motivoRejeicao:
            print(f"Motivo: {solicitacao.motivoRejeicao}")


def entrar():
    cpf, senha = ler_cpf_senha()
    clientes, contas, _ = carregar_dados()
    cliente = autenticar(cpf, senha, clientes)
    if cliente is None:
        print("CPF ou senha inválidos.")
        return

    print(f"\nBem-vindo(a), {cliente.nome}!")
    for conta in contas.values():
        if conta.titular.cpf == cliente.cpf:
            print(f"Conta nº {conta.numeroConta} | Saldo: R$ {conta.saldo:.2f}")
    print("(demais operações em desenvolvimento)")


if __name__ == "__main__":
    # Se não existir o arquivo, gera os dados e grava o arquivo
    if not os.path.isfile(arquivoClientes):
        clientes: dict[str,Cliente] = gerar_clientes()
        gravar_clientes(clientes, arquivoClientes)
        print("Arquivo Clientes gravado")
    else:
        # leitura de clientes
        clientes: dict[str,Cliente] =  carregar_clientes(arquivoClientes)
        print("Lendo arquivo Clientes...") 

    if not os.path.isfile(arquivoContas):
        contas: dict[int,Conta] = gerar_contas(clientes)
        gravar_contas(contas, arquivoContas)
        print("Arquivo Contas gravado")
    else:
        # leitura de contas
        contas: dict[int,Conta] = carregar_contas(arquivoContas)
        print("Lendo arquivo Contas...")

    #   Printar Clientes
    print(clientes)

    print("\n\n")

    #   Printar Contas
    print(contas)

    # Menu da página inicial do cliente
    while True:
        print_menu_inicial()
        match ler_opcao():
            case 1:
                entrar()
            case 2:
                solicitar_abertura_de_conta()
            case 3:
                acompanhar_solicitacao()
            case 0:
                print("Saindo...")
                break
            case _:
                print("Opção inválida.")