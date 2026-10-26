import re

class Cliente:
    def __init__(self, nome: str, cpf: str, telefone: str, email: str, senha: str):
        # atribuindo sem apara que o python valide o objeto na criaçao
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.senha = senha

    # NOME
    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("O nome não pode estar vazio.")
        self._nome = valor.strip().title()

    # CPF 
    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, valor: str):
        # Remove qualquer caractere que não seja número (ex: pontos e traços)
        cpf_limpo = re.sub(r'\D', '', valor)
        if len(cpf_limpo) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos.")
        self._cpf = cpf_limpo

    # TELEFONE 
    @property
    def telefone(self) -> str:
        return self._telefone

    @telefone.setter
    def telefone(self, valor: str):
        tel_limpo = re.sub(r'\D', '', valor)
        if len(tel_limpo) < 10 or len(tel_limpo) > 11:
            raise ValueError("Telefone inválido. Insira o DDD e o número.")
        self._telefone = tel_limpo

    #  E-MAIL 
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if "@" not in valor or "." not in valor:
            raise ValueError("E-mail com formato inválido.")
        self._email = valor.strip().lower()

    #  SENHA 
    @property
    def senha(self) -> str:
        return self._senha

    @senha.setter
    def senha(self, valor: str):
        if len(valor) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres para a segurança do banco.")
        self._senha = valor

    # --- REPRESENTAÇÃO ---
    def __repr__(self) -> str:
        return (
            f"Cliente(nome={self.nome!r}, "
            f"cpf={self.cpf!r}, "
            f"telefone={self.telefone!r}, "
            f"email={self.email!r})"
            # A senha nao esta aqui por conta de segurança
        )