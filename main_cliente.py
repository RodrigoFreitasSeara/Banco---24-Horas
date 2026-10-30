from serializacao import (
    carregar_clientes,
    carregar_contas,
    gerar_clientes,
    gerar_contas,
    gravar_clientes,
    gravar_contas,
)
import os.path
from cliente import Cliente
from conta import Conta
from interface import cli

arquivoClientes = "clientes.pkl" 
arquivoContas = "contas.pkl" 

if __name__ == "__main__":
    cli.interface_login()