from persistencia import *
import os.path
arquivoClientes = "clientes.pkl" 
arquivoContas = "contas.pkl" 

if __name__ == "__main__":
    # Se não existir o arquivo, gera os dados e grava o arquivo
    clientes: dict[str,Cliente] = gerar_clientes()
    contas: dict[int,Conta] = gerar_contas(clientes)

    if not os.path.isfile(arquivoClientes):
        gravar_clientes(clientes, arquivoClientes)
        print("Arquivo Clientes gravado")
    else:
        # leitura de clientes
        clientes: dict[str,Cliente] =  carregar_clientes(arquivoClientes)
        print("Lendo arquivo Clientes...") 

    if not os.path.isfile(arquivoContas):
        gravar_contas(contas, arquivoContas)
        print("Arquivo Contas gravado")
    else:
        # leitura de contas
        contas1: dict[int,Conta] = carregar_contas(arquivoContas)
        
    #   Printar Clientes
        print(clientes)

        print("\n\n")

    #   Printar Contas
        print(contas)

