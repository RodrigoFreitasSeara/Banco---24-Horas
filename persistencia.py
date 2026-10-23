from cliente import Cliente
from conta import Conta

import pickle

def gerar_clientes() -> dict[str,Cliente]:
    clientes: dict[str,Cliente] = dict()

    tempCpf = "16122561479"
    clientes[tempCpf] = Cliente("João", tempCpf, telefone="73956471229")

    tempCpf = "98694044722"
    clientes[tempCpf] = Cliente("Felipe", tempCpf, telefone="77920651465")

    tempCpf = "94192424207"
    clientes[tempCpf] = Cliente("Maria", tempCpf, telefone="71942565338")

    return clientes

def gerar_contas(clientes: dict[str,Cliente]) -> dict[int,Conta]:
    # Cria uma conta para cada cliente
    contas = dict()
    for cliente in clientes.items(): # cliente é uma tupla de tmpcpf com cliente
        #contas.append(Conta(cliente))
        contas[Conta.contasCriadas] = Conta(cliente[1])

    return contas


def gravar_clientes(clientes: dict[str,Cliente], pathArquivo: str):
    with open(pathArquivo, "wb") as arq:
        pickle.dump(clientes, arq)


def gravar_contas(contas: dict[int,Conta], pathArquivo: str):    
    with open(pathArquivo, "wb") as arq:
        pickle.dump(contas, arq)

def carregar_contas(pathArquivo: str) -> dict[int,Conta]:    
    with open(pathArquivo, "rb") as arq:
            contas: dict[int,Conta] = pickle.load(arq)
            return contas


def carregar_clientes(pathArquivo: str) -> dict[str,Cliente]:
    with open(pathArquivo, "rb") as arq:
        clientes: dict[str,Cliente] = pickle.load(arq)
        return clientes
        # TODO: finalizar sistema de leitura

