"""
Suíte de Testes End-to-End (E2E) Automatizados
Projeto: Banco 24 Horas - LP3 (UESC)
Valida a integração completa entre CLI, Controladora, Domínio POO e Persistência em Disco.
"""
import os
import sys
import unittest
from decimal import Decimal
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from cliente import Cliente
from conta import Conta
from solicitacao import Solicitacao, Status
from persistencia import Banco
from controladora import BancoControlador


class TestesE2EBanco(unittest.TestCase):
    ARQUIVO_TESTE = BASE_DIR / "dados_banco_e2e_teste.pkl"

    def setUp(self):
        # Garante ambiente de teste limpo
        if self.ARQUIVO_TESTE.exists():
            self.ARQUIVO_TESTE.unlink()
        tmp = self.ARQUIVO_TESTE.with_suffix(".tmp")
        if tmp.exists():
            tmp.unlink()

        self.banco = Banco()
        self.banco.ARQUIVO_DADOS = self.ARQUIVO_TESTE
        self.ctrl = BancoControlador(self.banco)

    def tearDown(self):
        # Limpeza pós-teste
        if self.ARQUIVO_TESTE.exists():
            self.ARQUIVO_TESTE.unlink()
        tmp = self.ARQUIVO_TESTE.with_suffix(".tmp")
        if tmp.exists():
            tmp.unlink()

    def test_cenario_01_inicializacao_limpa(self):
        """Cenário 01: Inicialização e gravação de base limpa."""
        self.banco.salvar_sistema()
        self.assertTrue(self.ARQUIVO_TESTE.exists(), "O arquivo .pkl deve ser criado em disco.")
        self.assertEqual(len(self.banco.clientes), 0)
        self.assertEqual(len(self.banco.contas), 0)
        self.assertEqual(len(self.banco.solicitacoes), 0)

    def test_cenario_02_e_03_cadastro_cliente_e_bloqueio_duplicidade(self):
        """Cenário 02 e 03: Cadastro de cliente com validações e bloqueio de CPF duplicado."""
        cliente = Cliente(
            nome="Carlos Drummond",
            cpf="12345678901",
            telefone="73988887777",
            email="carlos@uesc.br",
            senha="segredoForte123",
        )
        self.ctrl.cadastrar_cliente(cliente)
        self.assertEqual(len(self.banco.clientes), 1)

        # Tentativa de duplicidade de CPF
        cliente_duplicado = Cliente(
            nome="Carlos Outro",
            cpf="12345678901",
            telefone="73999990000",
            email="carlos.outro@uesc.br",
            senha="outraSenha123",
        )
        with self.assertRaises(ValueError) as ctx:
            self.ctrl.cadastrar_cliente(cliente_duplicado)
        self.assertIn("já cadastrado", str(ctx.exception))

    def test_cenario_04_autenticacao_cliente(self):
        """Cenário 04: Autenticação via PBKDF2-HMAC-SHA256."""
        cliente = Cliente(
            nome="Clarice Lispector",
            cpf="98765432100",
            telefone="73911112222",
            email="clarice@uesc.br",
            senha="senhaClarice123",
        )
        self.ctrl.cadastrar_cliente(cliente)

        # Senha incorreta
        auth_falha = self.ctrl.autenticar_cliente("98765432100", "senhaErrada")
        self.assertIsNone(auth_falha)

        # CPF inexistente
        auth_inexistente = self.ctrl.autenticar_cliente("00000000000", "senhaClarice123")
        self.assertIsNone(auth_inexistente)

        # Senha correta
        auth_sucesso = self.ctrl.autenticar_cliente("98765432100", "senhaClarice123")
        self.assertIsNotNone(auth_sucesso)
        self.assertEqual(auth_sucesso.nome, "Clarice Lispector")

    def test_cenario_05_e_06_solicitacao_abertura_conta_e_bloqueio_duplicada(self):
        """Cenário 05 e 06: Solicitação de abertura e impedimento de solicitação duplicada pendente."""
        cliente = Cliente(
            nome="Joao Guimaraes",
            cpf="11122233344",
            telefone="73933334444",
            email="joao@uesc.br",
            senha="senhaJoao123",
        )
        self.ctrl.cadastrar_cliente(cliente)

        solicitacao = self.ctrl.solicitar_abertura_conta(cliente)
        self.assertEqual(solicitacao.status, Status.PENDENTE)
        self.assertEqual(solicitacao.cliente.cpf, "11122233344")

        # Tentativa de nova solicitação enquanto a anterior está pendente
        with self.assertRaises(ValueError) as ctx:
            self.ctrl.solicitar_abertura_conta(cliente)
        self.assertIn("Já existe uma solicitação pendente", str(ctx.exception))

    def test_cenario_07_e_08_aprovacao_gerente_e_vinculacao_conta(self):
        """Cenário 07 e 08: Aprovação pelo gerente, criação da conta e vinculação ao cliente."""
        cliente = Cliente(
            nome="Graciliano Ramos",
            cpf="22233344455",
            telefone="73944445555",
            email="graciliano@uesc.br",
            senha="senhaGra123",
        )
        self.ctrl.cadastrar_cliente(cliente)
        sol = self.ctrl.solicitar_abertura_conta(cliente)

        # Gerente lista pendentes
        pendentes = self.ctrl.listar_solicitacoes_pendentes()
        self.assertEqual(len(pendentes), 1)

        # Gerente aprova
        conta = self.ctrl.aprovar_solicitacao(sol)
        self.assertEqual(sol.status, Status.APROVADA)
        self.assertEqual(conta.titular.cpf, "22233344455")
        self.assertEqual(conta.saldo, Decimal("0.00"))

        # Verifica vinculação bidirecional POO
        contas_cliente = self.ctrl.obter_contas_cliente(cliente)
        self.assertEqual(len(contas_cliente), 1)
        self.assertEqual(contas_cliente[0].numeroConta, conta.numeroConta)
        self.assertEqual(len(self.ctrl.listar_solicitacoes_pendentes()), 0)

    def test_cenario_09_deposito_com_historico(self):
        """Cenário 09: Depósito com validação positiva e registro de histórico."""
        cliente = Cliente(
            nome="Rachel de Queiroz",
            cpf="33344455566",
            telefone="73955556666",
            email="rachel@uesc.br",
            senha="senhaRachel123",
        )
        self.ctrl.cadastrar_cliente(cliente)
        conta = self.ctrl.cadastrar_conta(cliente)

        # Depósito inválido (negativo ou zero)
        with self.assertRaises(ValueError):
            self.ctrl.realizar_deposito(conta, 0)
        with self.assertRaises(ValueError):
            self.ctrl.realizar_deposito(conta, -50.0)

        # Depósito válido
        self.ctrl.realizar_deposito(conta, 1250.75)
        self.assertEqual(conta.saldo, Decimal("1250.75"))
        self.assertEqual(len(conta.historicoMovimentacoes), 1)
        self.assertEqual(conta.historicoMovimentacoes[0].tipo, "Depósito")
        self.assertEqual(conta.historicoMovimentacoes[0].direcao, "Crédito")

    def test_cenario_10_saque_limites_e_saldo_insuficiente(self):
        """Cenário 10: Saque com trava de saldo insuficiente e dedução correta."""
        cliente = Cliente(
            nome="Machado de Assis",
            cpf="44455566677",
            telefone="73966667777",
            email="machado@uesc.br",
            senha="senhaMachado123",
        )
        self.ctrl.cadastrar_cliente(cliente)
        conta = self.ctrl.cadastrar_conta(cliente)
        self.ctrl.realizar_deposito(conta, 500.00)

        # Saque maior que o saldo
        with self.assertRaises(ValueError) as ctx:
            self.ctrl.realizar_saque(conta, 500.01)
        self.assertIn("Saldo insuficiente", str(ctx.exception))

        # Saque válido
        self.ctrl.realizar_saque(conta, 200.00)
        self.assertEqual(conta.saldo, Decimal("300.00"))
        self.assertEqual(len(conta.historicoMovimentacoes), 2)
        self.assertEqual(conta.historicoMovimentacoes[1].tipo, "Saque")
        self.assertEqual(conta.historicoMovimentacoes[1].direcao, "Débito")

    def test_cenario_11_transferencia_interbancaria(self):
        """Cenário 11: Transferência atômica entre duas contas com extrato cruzado."""
        c1 = Cliente("Aluisio Azevedo", "55566677788", "73977778888", "aluisio@uesc.br", "senhaAluisio1")
        c2 = Cliente("Lima Barreto", "66677788899", "73988889999", "lima@uesc.br", "senhaLima123")
        self.ctrl.cadastrar_cliente(c1)
        self.ctrl.cadastrar_cliente(c2)

        conta1 = self.ctrl.cadastrar_conta(c1)
        conta2 = self.ctrl.cadastrar_conta(c2)

        self.ctrl.realizar_deposito(conta1, 1000.00)

        # Transferência para a mesma conta (proibida)
        with self.assertRaises(ValueError) as ctx:
            self.ctrl.realizar_transferencia(conta1, conta1, 100.00)
        self.assertIn("mesma conta", str(ctx.exception))

        # Transferência com saldo insuficiente
        with self.assertRaises(ValueError) as ctx:
            self.ctrl.realizar_transferencia(conta1, conta2, 1200.00)
        self.assertIn("Saldo insuficiente", str(ctx.exception))

        # Transferência válida
        self.ctrl.realizar_transferencia(conta1, conta2, 450.00, modalidade="PIX")
        self.assertEqual(conta1.saldo, Decimal("550.00"))
        self.assertEqual(conta2.saldo, Decimal("450.00"))

        # Histórico da conta 1 (origem)
        self.assertTrue(any("enviada" in m.tipo for m in conta1.historicoMovimentacoes))
        # Histórico da conta 2 (destino)
        self.assertTrue(any("recebida" in m.tipo for m in conta2.historicoMovimentacoes))

    def test_cenario_12_remocao_segura_de_cliente(self):
        """Cenário 12: Bloqueio de remoção com saldo positivo e exclusão com saldo zerado."""
        cliente = Cliente("Jose de Alencar", "77788899900", "73999991111", "jose@uesc.br", "senhaJose123")
        self.ctrl.cadastrar_cliente(cliente)
        conta = self.ctrl.cadastrar_conta(cliente)
        self.ctrl.realizar_deposito(conta, 100.00)

        # Bloqueio de exclusão com saldo positivo
        with self.assertRaises(ValueError) as ctx:
            self.ctrl.remover_cliente(cliente.cpf)
        self.assertIn("saldo positivo", str(ctx.exception))

        # Zera saldo via saque
        self.ctrl.realizar_saque(conta, 100.00)
        self.assertEqual(conta.saldo, Decimal("0.00"))

        # Remoção autorizada
        self.ctrl.remover_cliente(cliente.cpf)
        self.assertIsNone(self.ctrl.obter_cliente(cliente.cpf))
        self.assertIsNone(self.ctrl.obter_conta(conta.numeroConta))

    def test_cenario_13_persistencia_recarga_disco(self):
        """Cenário 13: Validação de desserialização completa após encerramento do processo."""
        c = Cliente("Monteiro Lobato", "88899900011", "73922223333", "monteiro@uesc.br", "senhaMonteiro1")
        self.ctrl.cadastrar_cliente(c)
        conta = self.ctrl.cadastrar_conta(c)
        self.ctrl.realizar_deposito(conta, 875.50)

        # Simula reinício de aplicação abrindo novo Banco a partir do arquivo .pkl
        novo_banco = Banco()
        novo_banco.ARQUIVO_DADOS = self.ARQUIVO_TESTE
        novo_controlador = BancoControlador(novo_banco)

        cliente_rec = novo_controlador.obter_cliente(c.cpf)
        self.assertIsNotNone(cliente_rec)
        self.assertEqual(cliente_rec.nome, "Monteiro Lobato")

        conta_rec = novo_controlador.obter_conta(conta.numeroConta)
        self.assertIsNotNone(conta_rec)
        self.assertEqual(conta_rec.saldo, Decimal("875.50"))
        self.assertEqual(len(conta_rec.historicoMovimentacoes), 1)


if __name__ == "__main__":
    unittest.main()
