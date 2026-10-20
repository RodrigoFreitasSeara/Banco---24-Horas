
from cliente import Cliente

def print_menu_gerente():
    print("1. Cadastrar Cliente\n"
        "2. Remover Cliente\n"
        "0. Sair\n"
        "> ",
    end='')

def cadastrar_cliente() -> Cliente:
    print("Informe os seguintes dados:")
    nome = input("\tNome: ")
    cpf = input("\tCPF: ")
    telefone = input("\tTelefone: ")

    return Cliente(nome, cpf, telefone)

if __name__ == "__main__":
    while True:
        print_menu_gerente()
        entrada = int(input())
        if (entrada == 1):
            match entrada:
                case 1:
                    # TODO: implementar adição do novo cliente ao dicionário
                    novoCliente = cadastrar_cliente()
                    print("Novo Cliente:")
                    print(novoCliente)
                case 2:
                    print("...")
                case 0:
                    print("...")
                    break