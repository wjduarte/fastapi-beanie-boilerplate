# 🚀 TODOFast API - Pydantic V2 & Beanie ODM

API de gerenciamento de tarefas (ToDo) de alta performance, construída com foco em **escalabilidade**, **segurança** e **boas práticas modernas em Python**.

O projeto utiliza arquitetura assíncrona com **FastAPI**, integrada ao **MongoDB** via **Beanie ODM**.

---

## 🛠 Tecnologias e Padrões

- **FastAPI**: Framework web moderno e de alta performance.
- **Pydantic V2**: Validação e serialização extremamente rápidas.
- **Beanie ODM**: Mapeamento de documentos MongoDB baseado em tipos Python.
- **Motor**: Driver assíncrono para MongoDB.
- **JWT (JSON Web Tokens)**: Autenticação com Access e Refresh Tokens.
- **Argon2**: Hash de senhas de última geração para máxima segurança.

---

## 🏗 Arquitetura do Projeto

Estrutura modular para facilitar manutenção, escalabilidade e testes:

```text
app/
├── api/              # Camada de entrada (Handlers e Rotas)
│   ├── api_v1/       # Versão 1 da API
│   └── auth/         # Autenticação e JWT
├── core/             # Configurações globais e segurança
├── models/           # Modelos de dados (Beanie Documents)
├── schemas/          # Schemas de validação (Pydantic)
├── services/         # Regras de negócio
└── app.py            # Ponto de entrada e Lifespan
```


## 🔐 Funcionalidades Principais

### 🔑 Autenticação e Segurança
- Registro de usuários
- Login via OAuth2 (JWT)
- Renovação de acesso com Refresh Token
- Hash de senhas com Argon2

### 📝 Gerenciamento de Tarefas
- CRUD completo de tarefas
- Tarefas vinculadas ao usuário autenticado
- Autorização em nível de objeto (Object-Level Authorization)

### 🔎 Busca Inteligente
- Filtro por título (Regex Case-Insensitive)
- Filtro por status da tarefa

### 📄 Documentação Automática
- Swagger UI
- ReDoc

---

## 🚀 Como Rodar o Projeto

### 📋 Pré-requisitos
- Python **3.10+**
- MongoDB local ou MongoDB Atlas

---

### 1️⃣ Clonar e Instalar

```bash
git clone https://github.com/seu-usuario/todofast-api.git
cd todofast-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto seguindo o modelo abaixo:

```env
PROJECT_NAME="TODOFast API"
MONGO_CONNECTION_STRING="mongodb://localhost:27017/todofast"
JWT_SECRET_KEY="sua_chave_secreta_access"
JWT_REFRESH_SECRET_KEY="sua_chave_secreta_refresh"
```

### 3️⃣ Executar o Servidor

Execute o comando abaixo para iniciar a aplicação:

```bash
uvicorn app.app:app --reload
```

Acesse a documentação interativa em:

- **Swagger UI**: http://127.0.0.1:8000/docs

---

## 📖 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/auth/login` | Autentica usuário e retorna tokens |
| POST | `/api/v1/auth/refresh` | Gera novo access token via refresh token |
| POST | `/api/v1/users/create` | Registra um novo usuário |
| GET | `/api/v1/tasks/` | Lista tarefas do usuário com filtros |
| POST | `/api/v1/tasks/create` | Cria uma nova tarefa vinculada ao usuário |

---

Desenvolvido com ☕ e foco em excelência técnica.
