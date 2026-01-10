🚀 TODOFast API - Pydantic V2 & Beanie ODM
Esta é uma API de gerenciamento de tarefas (ToDo) de alta performance, construída com foco em escalabilidade, segurança e práticas modernas de desenvolvimento Python. O projeto utiliza a arquitetura assíncrona do FastAPI integrada ao MongoDB através do Beanie ODM.

🛠 Tecnologias e Padrões
FastAPI: Framework web moderno e de alta performance.

Pydantic V2: Validação de dados e serialização extremamente rápida.

Beanie ODM: Mapeamento de documentos MongoDB baseado em tipos Python.

Motor: Driver assíncrono para MongoDB.

JWT (JSON Web Tokens): Autenticação robusta com Access e Refresh Tokens.

Argon2: Algoritmo de hash de senhas de última geração para segurança máxima.

🏗 Arquitetura do Projeto
O projeto segue uma estrutura modular para facilitar a manutenção e testes:

app/
├── api/              # Camada de entrada (Handlers e Rotas)
│   ├── api_v1/       # Versão 1 da API
│   └── auth/         # Lógica de autenticação e JWT
├── core/             # Configurações globais e segurança
├── models/           # Modelos de dados (Beanie Documents)
├── schemas/          # Esquemas de validação (Pydantic Models)
├── services/         # Regras de negócio e lógica de persistência
└── app.py            # Ponto de entrada e configuração do Lifespan

🔐 Funcionalidades Principais
Auth System: Registro de usuários, Login via OAuth2 e renovação de acesso via Refresh Token.

Task Management: CRUD completo de tarefas vinculado ao usuário logado (Object-Level Authorization).

Smart Search: Filtros de busca por título (Regex Case-Insensitive) e status.

Automated Docs: Documentação interativa via Swagger UI e ReDoc.

🚀 Como Rodar o Projeto
Pré-requisitos
Python 3.10+

MongoDB rodando localmente ou via Atlas.

1. Clonar e Instalar

git clone https://github.com/seu-usuario/todofast-api.git
cd todofast-api
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt

2. Variáveis de Ambiente

Crie um arquivo .env na raiz do projeto seguindo o modelo:

PROJECT_NAME="TODOFast API"
MONGO_CONNECTION_STRING="mongodb://localhost:27017/todofast"
JWT_SECRET_KEY="sua_chave_secreta_para_access_token"
JWT_REFRESH_SECRET_KEY="outra_chave_secreta_para_refresh"

3. Executar o Servidor

uvicorn app.app:app --reload

Acesse a documentação em: http://127.0.0.1:8000/docs

📖 Endpoints Principais

Método,Endpoint,Descrição
POST,/api/v1/auth/login,Autentica usuário e retorna tokens.
POST,/api/v1/auth/refresh,Gera novo access_token via refresh_token.
POST,/api/v1/users/create,Registra um novo usuário.
GET,/api/v1/tasks/,Lista tarefas do usuário com filtros.
POST,/api/v1/tasks/create,Cria uma nova tarefa vinculada ao usuário.

Desenvolvido com ☕ e foco em excelência técnica.
