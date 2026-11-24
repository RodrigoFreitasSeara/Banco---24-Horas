"""Leitura e sanitização de dados no terminal, compartilhada pelos menus."""
import re
from getpass import getpass
from cliente import Cliente


def ler_dados_cliente() -> Cliente:
    """Pede os dados do cadastro. Lança ValueError se algum for inválido."""
    print("Informe os seguintes dados:")
    nome = input("\tNome: ").strip()
    cpf = input("\tCPF: ").strip()
    telefone = input("\tTelefone (com DDD): ").strip()
    email = input("\tE-mail: ").strip()
    senha = getpass("\tSenha (mín. 6 caracteres): ")
    confirmacao = getpass("\tConfirme a senha: ")

    if senha != confirmacao:
        raise ValueError("As senhas não conferem.")

    return Cliente(nome, cpf, telefone, email, senha)


def ler_cpf_senha() -> tuple[str, str]:
    """Lê CPF e senha de forma mascarada."""
    cpf = re.sub(r"\D", "", input("\tCPF: "))
    senha = getpass("\tSenha: ")
    return cpf, senha


def ler_cpf_cliente(mensagem: str = "\tInforme o CPF do cliente: ") -> str:
    """Lê apenas o CPF sanitizado (apenas números)."""
    return re.sub(r"\D", "", input(mensagem))


def ler_opcao() -> int | None:
    """Lê uma opção inteira do menu ou retorna None em caso de entrada não-numérica."""
    try:
        entrada = input().strip()
        return int(entrada)
    except ValueError:
        return None


def ler_valor(mensagem: str = "\tValor (R$): ") -> float:
    """Lê um valor monetário positivo, aceitando ponto ou vírgula decimal."""
    texto = input(mensagem).strip().replace(",", ".")
    try:
        val = float(texto)
        if val <= 0:
            raise ValueError("O valor deve ser estritamente maior que zero.")
        return val
    except ValueError as e:
        if "estritamente maior que zero" in str(e):
            raise
        raise ValueError("Valor monetário inválido. Digite um número como 100.00 ou 100,50.")
