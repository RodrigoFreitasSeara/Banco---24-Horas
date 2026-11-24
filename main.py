"""
Ponto de Entrada Central e Orquestrador Unificado
Projeto: Banco 24 Horas
Linguagem de Programação 3 (LP3) - Universidade Estadual de Santa Cruz (UESC)
"""
from interface import cli
from entrada import ler_opcao


def main() -> None:
    while True:
        print("\n" + "=" * 60)
        print("          BANCO 24 HORAS - SISTEMA BANCÁRIO INTEGRADO")
        print("    Linguagem de Programação 3 - UESC (Ilhéus - Bahia)")
        print("=" * 60)
        print("Integrantes do Grupo:")
        print("  • Rafael Mota          • Arthur de Carvalho")
        print("  • André Felipe         • Rodrigo Freitas")
        print("  • Amanda Lopes")
        print("-" * 60)
        print("1. Portal do Cliente (Login / Cadastro / Transações)")
        print("2. Portal da Gerência (Aprovações / Contas / Gestão)")
        print("0. Encerrar o Sistema")
        print("=" * 60)
        print("Selecione uma opção: ", end="")

        match ler_opcao():
            case 1:
                cli.interface_login()
            case 2:
                cli.interface_gerente()
            case 0:
                print("\nEncerrando o Banco 24 Horas. Obrigado por utilizar nossos serviços!")
                break
            case _:
                print("\nOpção inválida! Escolha 1, 2 ou 0.")


if __name__ == "__main__":
    main()
