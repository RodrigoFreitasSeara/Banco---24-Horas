# Banco 24 Horas — Sistema Bancário Integrado

Sistema bancário completo orientado a objetos para terminal CLI, desenvolvido para a disciplina de **Linguagem de Programação 3 (LP3)** do curso de Ciência da Computação **Universidade Estadual de Santa Cruz (UESC)**.

---

## 👥 Equipe de Desenvolvimento
- **Rafael Mota**
- **Arthur de Carvalho**
- **André Felipe**
- **Rodrigo Freitas**
- **Amanda Lopes**

---

## 🎯 Objetivo e Diretrizes Acadêmicas

O projeto tem como objetivo exercitar conceitos avançados de **Programação Orientada a Objetos (POO)** e fluxo transacional:
- **Modelagem Orientada a Objetos:** Classes de domínio com encapsulamento rigoroso, agregação, composição, relacionamentos bidirecionais (`Cliente` $\leftrightarrow$ `Conta`), sobrecarga de operadores (`__eq__`, `__hash__`) e separação em camadas (Domínio, Repositórios, Fachada Controladora e View CLI).
- **Persistência Estrita em Disco (Serialização):** Todo o estado do banco é armazenado em disco utilizando exclusivamente a biblioteca padrão `pickle`, com gravação atômica (`os.replace`) contra corrupção de arquivos.
- **Sem Banco Relacional e Sem Rede:** Conforme as restrições da disciplina, o sistema não utiliza SQLite, SQL externo ou comunicação via rede/sockets.

---

## 🏗️ Arquitetura de Software e Módulos

```
Banco---24-Horas/
├── main.py                  # Ponto de entrada do sistema
│
├── cliente.py               # Entidade Cliente e Coleção Clientes (Repositório)
├── conta.py                 # Entidade Conta, Coleção Contas e HistoricoMovimentacoes
├── movimentacao.py          # Objeto de Valor Movimentacao (Crédito / Débito)
├── solicitacao.py           # Entidade Solicitacao e Repositório Solicitacoes
├── seguranca.py             # Criptografia de senhas (PBKDF2-HMAC-SHA256, recomendação OWASP)
│
├── controladora.py          # BancoControlador (Camada de Serviço / Fachada de Aplicação)
├── interface.py             # Classe Cli (Camada de Apresentação e Menus do Usuário)
├── entrada.py               # Sanitização e leitura de dados no terminal
├── persistencia.py          # Agregado Raiz Banco e gerenciador de persistência atômica
│
└── .gitignore               # Configurações de versionamento (ignora *.pkl e *.tmp)
```

---

## ⚙️ Funcionalidades do Sistema

### 👤 Portal do Cliente
- **Cadastro e Validação:** Validação estrita de CPF (11 dígitos), telefone com DDD, e-mail via regex e senha forte (mínimo de 6 caracteres).
- **Segurança de Credenciais:** As senhas nunca são armazenadas em texto puro; utiliza-se salt aleatório e derivação PBKDF2-HMAC-SHA256.
- **Abertura de Conta:** Solicitação de abertura de conta com status `PENDENTE`, impedindo solicitações duplicadas.
- **Acompanhamento de Status:** Consulta em tempo real do andamento da solicitação (Pendente, Aprovada ou Rejeitada com justificativa).
- **Sessão Bancária Completa (Conta Ativa):**
  - **Extrato Consolidado:** Tabela temporal exibindo data/hora, tipo de operação, direção (`Crédito`/`Débito`), valor e saldo consolidado.
  - **Depósito:** Crédito imediato em conta com persistência automática em disco.
  - **Saque:** Débito com validação de saldo disponível.
  - **Transferência:** Transferência atômica entre contas distintas, atualizando os históricos e saldos de ambas as partes.

### 👔 Portal da Gerência
- **Autenticação Administrativa:** Protegido por senha de administrador (`admin123`).
- **Análise de Solicitações:** Fila interativa para aprovar (criando a conta vinculada automaticamente) ou rejeitar (com justificativa).
- **Cadastro de Clientes:** Cadastro direto de novos clientes pelo gerente.
- **Abertura de Conta:** Abertura de conta vinculada a um cliente já cadastrado.
- **Relatório Geral:** Listagem completa de todos os clientes cadastrados e suas respectivas contas ativas e saldos.
- **Remoção Segura de Clientes:** Trava de segurança que impede o encerramento de clientes que possuam saldo positivo retido em conta.

---

## 🚀 Como Executar

### Pré-requisitos
- **Python 3.10+** (Testado e homologado no Python 3.14).
- Nenhuma dependência externa necessária (utiliza exclusivamente a biblioteca padrão do Python).

### Execução Linux, macOS e demais sistemas POSIX
```bash
python3 main.py
```

### Execução Windows
```cmd
py main.py
```