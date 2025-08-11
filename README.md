## API de Finanças Pessoais

  

Essa API permite gerenciar transações financeiras, consultar saldo e autenticar usuários. Foi desenvolvida em **Python** utilizando **FastAPI**.

  

## 📌 Índice

- [Descrição](#-descrição)

- [Tecnologias](#-tecnologias)

- [Autenticação](#-autenticação)

- [Endpoints](#-endpoints)

- [Transações](#transações)

- [Saldo](#saldo)

- [Autenticação de Usuário](#autenticação-de-usuário)

- [Licença](#-licença)

  

**Descrição**

A API de Finanças Pessoais é um sistema para registrar, consultar, atualizar e excluir transações, além de calcular o saldo disponível.

Inclui autenticação com **JWT** para garantir a segurança dos dados.

  

## 🛠 Tecnologias

  

- **Python** 3.11+

- **FastAPI**

- **Uvicorn**

- **Pydantic**

- **Jose (PyJWT)**

  
  

## 📡 Endpoints

  

### 📂 Transações

  
  

| Método | Rota | Descrição |

| ------ | ----------------- | ----------------------------------- |

| GET |  `/transacao`  | Lista todas as transações |

| POST |  `/transacao`  | Cria nova transação |

| GET |  `/transacao/{id}`  | Retorna transação específica |

| PATCH |  `/transacao/{id}`  | Atualiza parcialmente uma transação |

| DELETE |  `/transacao/{id}`  | Remove uma transação |

  
  

Exemplo de criação (POST /transacao):

  

> JSON {
> 
> "descricao": "Salário",
> 
> "valor": 2500.00
> 
> }

  

💰 Saldo

  

| Método | Rota | Descrição |

| ------ | -------- | ------------------- |

| GET |  `/saldo`  | Retorna saldo atual |

  
  

Resposta exemplo:

  

> JSON {
> 
> "saldo": 3450.50
> 
> }

  

👤 Autenticação de Usuário

| Método | Rota | Descrição |

| ------ | ---------------- | ----------------------- |

| POST |  `/auth/register`  | Registra novo usuário |

| POST |  `/auth/login`  | Autentica e retorna JWT |

  
  

Login (POST /auth/login):

  
  

Editar

> JSON { 
> 
> "email": "joao@email.com",
> 
> "senha": "123456"
> 
> }

  

Resposta:

  

> JSON {
> 
> "token": "eyJhbGciOiJIUzI1..."
> 
> }
