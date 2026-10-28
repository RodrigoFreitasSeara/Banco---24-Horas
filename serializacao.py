from cliente import Cliente
from conta import Conta
from solicitacao import SolicitacaoConta

import os.path
import pickle

arquivoClientes = "clientes.pkl"
arquivoContas = "contas.pkl"
arquivoSolicitacoes = "solicitacoes.pkl"

def gerar_clientes() -> dict[str,Cliente]:
    clientes: dict[str,Cliente] = dict()

    tempCpf = "16122561479"
    clientes[tempCpf] = Cliente("João", tempCpf, "73956471229", "joao@email.com", "senha123")

    tempCpf = "98694044722"
    clientes[tempCpf] = Cliente("Felipe", tempCpf, "77920651465", "felipe@email.com", "senha123")

    tempCpf = "94192424207"
    clientes[tempCpf] = Cliente("Maria", tempCpf, "71942565338", "maria@email.com", "senha123")

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
            # o contador da classe não é salvo no pickle: reajusta para não repetir números
            Conta.contasCriadas = max(contas, default=0)
            return contas


def carregar_clientes(pathArquivo: str) -> dict[str,Cliente]:
    with open(pathArquivo, "rb") as arq:
        clientes: dict[str,Cliente] = pickle.load(arq)
        return clientes
        # TODO: finalizar sistema de leitura


def gravar_solicitacoes(solicitacoes: dict[int,SolicitacaoConta], pathArquivo: str):
    with open(pathArquivo, "wb") as arq:
        pickle.dump(solicitacoes, arq)


def carregar_solicitacoes(pathArquivo: str) -> dict[int,SolicitacaoConta]:
    with open(pathArquivo, "rb") as arq:
        return pickle.load(arq)


def carregar_dados():
    """Lê tudo do disco (dicionários vazios se os arquivos ainda não existem).

    Os dois menus (cliente e gerente) podem estar abertos ao mesmo tempo, então
    cada ação lê os arquivos de novo antes de mexer e grava logo em seguida.
    """
    clientes = carregar_clientes(arquivoClientes) if os.path.isfile(arquivoClientes) else {}
    contas = carregar_contas(arquivoContas) if os.path.isfile(arquivoContas) else {}
    solicitacoes = (carregar_solicitacoes(arquivoSolicitacoes)
                    if os.path.isfile(arquivoSolicitacoes) else {})
    return clientes, contas, solicitacoes


def salvar_dados(clientes, contas, solicitacoes):
    gravar_clientes(clientes, arquivoClientes)
    gravar_contas(contas, arquivoContas)
    gravar_solicitacoes(solicitacoes, arquivoSolicitacoes)