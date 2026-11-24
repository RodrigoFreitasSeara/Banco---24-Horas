from cliente import Clientes
from conta import Contas
from solicitacao import Solicitacoes
from pathlib import Path
import os
import pickle


class Banco:
    """Armazena o estado global do banco"""

    BASE_DIR = Path(__file__).resolve().parent
    ARQUIVO_DADOS = BASE_DIR / "dados_banco.pkl"

    def __init__(self) -> None:
        self.clientes = Clientes()  
        self.contas = Contas()
        self.solicitacoes = Solicitacoes()

    # Salvando o estado global atomicamente em disco
    def salvar_sistema(self) -> None:
        temp_arquivo = self.ARQUIVO_DADOS.with_suffix(".tmp")
        with open(temp_arquivo, "wb") as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(temp_arquivo, self.ARQUIVO_DADOS)

    # Carregando o estado global
    def carregar_sistema(self) -> "Banco":
        if not self.ARQUIVO_DADOS.exists():
            return self
        try:
            with open(self.ARQUIVO_DADOS, "rb") as f:
                dados = pickle.load(f)
                if isinstance(dados, Banco):
                    return dados
                return self
        except Exception:
            return self

