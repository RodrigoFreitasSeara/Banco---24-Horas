"""
Validação Interativa do CLI via Subprocesso
Simula entradas de teclado do usuário real no terminal para main.py
"""
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "dados_banco.pkl"
TMP_FILE = BASE_DIR / "dados_banco.tmp"

# Limpa base para o teste interativo
if DB_FILE.exists():
    DB_FILE.unlink()
if TMP_FILE.exists():
    TMP_FILE.unlink()

# Fluxo de entrada simulada no terminal:
# 1. Menu Principal: Opção 1 (Portal do Cliente)
# 2. Portal do Cliente: Opção 2 (Cadastro)
#    - Nome: Rafael Mota
#    - CPF: 11122233344
#    - Telefone: 73988889999
#    - Email: rafael@uesc.br
#    - Senha: senhaForte123
#    - Confirmação: senhaForte123
# 3. Menu Cliente Sem Conta: Opção 1 (Solicitar abertura de conta)
# 4. Opção 0 (Desconectar)
# 5. Opção 0 (Sair da tela de login do cliente)
# 6. Menu Principal: Opção 2 (Portal da Gerência)
#    - Senha admin: admin123
#    - Opção 3 (Analisar Solicitações Pendentes)
#    - Ação: a (Aprovar)
#    - Opção 0 (Sair da gerência)
# 7. Menu Principal: Opção 1 (Portal do Cliente)
#    - Opção 1 (Fazer Login)
#    - CPF: 11122233344
#    - Senha: senhaForte123
# 8. Sessão Bancária da Conta Aprovada:
#    - Opção 2 (Depósito): 1500.00
#    - Opção 3 (Saque): 300.00
#    - Opção 1 (Extrato)
#    - Opção 0 (Logout)
#    - Opção 0 (Sair login)
# 9. Menu Principal: Opção 0 (Encerrar o sistema)

entradas = [
    # 1. Acessa portal do cliente
    "1",
    # 2. Cadastro
    "2",
    "Rafael Mota",
    "11122233344",
    "73988889999",
    "rafael@uesc.br",
    "senhaForte123",
    "senhaForte123",
    # 3. Solicitar abertura de conta
    "1",
    # 4. Desconectar do portal cliente
    "0",
    # 5. Voltar ao menu principal
    "0",
    # 6. Acessar gerência
    "2",
    "admin123",
    "3",  # Analisar pendentes
    "a",  # Aprovar
    "0",  # Sair da gerência
    # 7. Acessar portal do cliente de novo
    "1",
    "1",  # Login
    "11122233344",
    "senhaForte123",
    # 8. Sessão bancária ativa
    "2",  # Depósito
    "1500.00",
    "3",  # Saque
    "300.00",
    "1",  # Extrato
    "0",  # Logout da conta
    "0",  # Voltar menu login
    # 9. Encerrar
    "0",
]

entrada_texto = "\n".join(entradas) + "\n"

resultado = subprocess.run(
    [sys.executable, str(BASE_DIR / "main.py")],
    input=entrada_texto,
    text=True,
    capture_output=True,
)

print("CÓDIGO DE RETORNO:", resultado.returncode)
print("--- STDOUT ---")
print(resultado.stdout)

if resultado.returncode == 0 and "Saldo atual disponível:" in resultado.stdout:
    print(">>> SUCESSO TOTAL NO TESTE DE CLI INTERATIVO! <<<")
else:
    print("--- STDERR ---")
    print(resultado.stderr)
    sys.exit(1)
