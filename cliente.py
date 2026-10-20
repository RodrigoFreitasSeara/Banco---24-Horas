class Cliente:
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

