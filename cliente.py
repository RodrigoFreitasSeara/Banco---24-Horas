class Cliente:
    """ Classe para cliente individual """

    def __init__(self, nome: str, cpf: str, telefone: str):
        # TODO: definir restrições e tratamentos para os tipos de dados 
        # TODO: adicionar e-mail e senha
        self.nome = nome
        self.cpf = cpf 
        self.telefone = telefone

    def __repr__(self) -> str:
        return (
            f"Cliente(nome={self.nome!r}, "
            f"cpf={self.cpf!r}, "
            f"telefone={self.telefone!r})"
        )

class Clientes:
    """ Classe para controle de todos os clientes do sistema"""

    def __init__():
        # TODO: trocar str por cpf quando esse tipo de dado for criado
        # TODO: Adcionar lógica de instanciar o objeto somente quando  
        # o programa tentar acessá-lo quando ele não existir, com objetivo
        # de ter somente um objeto global desta classe
        
        _dictClientes: dict[str, Cliente] = dict()

    # TODO: implementar função abaixo
    # def obter_cliente(cpf: str):
