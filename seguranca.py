"""Módulo de segurança:

Usa PBKDF2-HMAC-SHA256,com salt aleatório por senha e comparação em tempo constante.

Formato armazenado:  pbkdf2_sha256$<iterações>$<salt em base64>$<hash em base64>
Guardar as iterações junto do hash permite aumentá-las no futuro sem
invalidar as senhas já cadastradas.
"""
import base64
import hashlib
import hmac
import secrets

ALGORITMO = "pbkdf2_sha256"
ITERACOES = 600_000   # recomendação OWASP para PBKDF2-HMAC-SHA256
TAMANHO_SALT = 16     # bytes


def _b64(dados: bytes) -> str:
    return base64.b64encode(dados).decode("ascii")


def gerar_hash_senha(senha: str) -> str:
    """Recebe a senha em texto puro e devolve a string pronta para armazenar."""
    salt = secrets.token_bytes(TAMANHO_SALT)
    derivada = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, ITERACOES)
    return f"{ALGORITMO}${ITERACOES}${_b64(salt)}${_b64(derivada)}"


def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    """Confere se a senha digitada corresponde ao hash armazenado."""
    try:
        algoritmo, iteracoes, salt_b64, hash_b64 = hash_armazenado.split("$")
        if algoritmo != ALGORITMO:
            return False
        iteracoes = int(iteracoes)
        salt = base64.b64decode(salt_b64)
        esperado = base64.b64decode(hash_b64)
    except (ValueError, AttributeError):   # formato corrompido
        return False

    calculado = hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), salt, iteracoes, dklen=len(esperado)
    )
    return hmac.compare_digest(calculado, esperado)