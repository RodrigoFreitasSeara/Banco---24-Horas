"""Leitura de dados no terminal, compartilhada pelos menus do cliente e do gerente."""
import re
from getpass import getpass

from cliente import Cliente


def ler_dados_cliente() -> Cliente:
    """Pede os dados do cadastro. Lança ValueError se algum for inválido."""
    print("Informe os seguintes dados:")
    nome = input("\tNome: ")
    cpf = input("\tCPF: ")
    telefone = input("\tTelefone (com DDD): ")
    email = input("\tE-mail: ")
    senha = getpass("\tSenha (mín. 6 caracteres): ")
    confirmacao = getpass("\tConfirme a senha: ")

    if senha != confirmacao:
        raise ValueError("As senhas não conferem.")

    return Cliente(nome, cpf, telefone, email, senha)


def ler_cpf_senha() -> tuple[str, str]:
    cpf = re.sub(r"\D", "", input("\tCPF: "))
    senha = getpass("\tSenha: ")
    return cpf, senha


def ler_opcao() -> int | None:
    try:
        return int(input())
    except ValueError:
        return None
