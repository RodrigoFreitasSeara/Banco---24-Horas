from cliente import Clientes
from conta import Contas
from solicitacao import Solicitacoes
from pathlib import Path
import pickle


class Banco:
    """Armazena o estado global do banco"""

    ARQUIVO_DADOS = Path("dados_banco.pkl")

    def __init__(self) -> None:
        self.clientes = Clientes()  
        self.contas = Contas()
        self.solicitacoes = Solicitacoes()


    # Salvando o estado global
    def salvar_sistema(self) -> None:
        with open(self.ARQUIVO_DADOS, "wb") as f:
            pickle.dump(self.ARQUIVO_DADOS, f)


    # Carregando o estado global
    def carregar_sistema(self) -> Banco:
        if not self.ARQUIVO_DADOS.exists():
            return Banco()
        with open(self.ARQUIVO_DADOS, "rb") as f:
            return pickle.load(f)
