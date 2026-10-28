from cliente import Cliente
from conta import Conta
from entrada import ler_dados_cliente, ler_opcao
from serializacao import carregar_dados, salvar_dados
from solicitacao import aprovar, listar_pendentes, rejeitar


def print_menu_gerente():
    _, _, solicitacoes = carregar_dados()
    pendentes = len(listar_pendentes(solicitacoes))
    print("\n1. Cadastrar Cliente e Criar Conta\n"
          "2. Remover Cliente\n"
          f"3. Solicitações de abertura de conta ({pendentes} pendente(s))\n"
          "0. Sair\n"
          "> ", end='')


def cadastrar_cliente_e_criar_conta(cliente: Cliente,clientes: dict[str, Cliente],contas: dict[int, Conta]) -> Conta:
    """Registra o cliente e abre a conta dele. Lança ValueError se o CPF já existir."""
    if cliente.cpf in clientes:
        raise ValueError("Já existe um cliente cadastrado com este CPF.")

    conta = Conta(cliente)
    clientes[cliente.cpf] = cliente
    contas[conta.numeroConta] = conta
    return conta


def cadastrar_direto():
    try:
        novoCliente = ler_dados_cliente()
        clientes, contas, solicitacoes = carregar_dados()
        conta = cadastrar_cliente_e_criar_conta(novoCliente, clientes, contas)
    except ValueError as erro:
        print(f"Cadastro não realizado: {erro}")
        return

    salvar_dados(clientes, contas, solicitacoes)
    print("\nCliente cadastrado com sucesso!")
    print(novoCliente)
    print(f"Conta criada: nº {conta.numeroConta}")


def analisar_solicitacoes():
    while True:
        clientes, contas, solicitacoes = carregar_dados()
        pendentes = listar_pendentes(solicitacoes)
        if not pendentes:
            print("Nenhuma solicitação pendente.")
            return

        print("\nSolicitações pendentes:")
        for s in pendentes:
            c = s.cliente
            print(f"  [{s.id}] {c.nome} | CPF {c.cpf} | {c.email} | "
                  f"tel {c.telefone} | {s.dataSolicitacao:%d/%m/%Y %H:%M}")

        try:
            escolhido = int(input("Nº da solicitação para analisar (0 para voltar): "))
        except ValueError:
            print("Opção inválida.")
            continue
        if escolhido == 0:
            return
        if escolhido not in {s.id for s in pendentes}:
            print("Solicitação não encontrada.")
            continue

        acao = input("[A]provar, [R]ejeitar ou [V]oltar: ").strip().lower()
        try:
            if acao == "a":
                conta = aprovar(escolhido, clientes, contas, solicitacoes)
                salvar_dados(clientes, contas, solicitacoes)
                print(f"Aprovada! Conta nº {conta.numeroConta} criada.")
            elif acao == "r":
                motivo = input("Motivo da rejeição (opcional): ")
                rejeitar(escolhido, solicitacoes, motivo)
                salvar_dados(clientes, contas, solicitacoes)
                print("Solicitação rejeitada.")
        except ValueError as erro:
            print(f"Não foi possível concluir: {erro}")


if __name__ == "__main__":
    while True:
        print_menu_gerente()
        match ler_opcao():
            case 1:
                cadastrar_direto()
            case 2:
                print("...")  # TODO: remover cliente
            case 3:
                analisar_solicitacoes()
            case 0:
                print("Saindo...")
                break
            case _:
                print("Opção inválida.")