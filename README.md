<<<<<<< HEAD
# 🚀 FastAPI + Beanie + Pydantic V2 (SaaS Boilerplate)


Este repositório serve como uma base sólida e extensível para o desenvolvimento de aplicações SaaS assíncronas utilizando Python. A arquitetura foi desenhada para suportar multi-tenancy e isolamento de dados.

## 🚀 Tecnologias Utilizadas
- **FastAPI**: Framework web de alta performance.
- **Beanie (ODM)**: Integração assíncrona com MongoDB.
- **Pydantic V2**: Validação de dados rigorosa e rápida.
- **JWT Auth**: Sistema de autenticação com Access e Refresh Tokens.
- **Pytest**: Suíte de testes automatizados com cobertura de integração.

## 🏗️ Principais Funcionalidades Implementadas
- [x] **Autenticação Segura**: Fluxo completo de registro, login e proteção de rotas.
- [x] **Isolamento de Dados (Multi-tenancy)**: Cada registro é vinculado a um `owner_id`.
- [x] **Relacionamentos Dinâmicos**: Implementação de tarefas vinculadas a categorias.
- [x] **Arquitetura de Testes**: 9 testes de integração cobrindo Auth, Tasks e Categories.
- [x] **Pydantic V2 Migration**: Código 100% atualizado para evitar depreciações.

## 🛠️ Como Iniciar
1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv .venv`
3. Instale as dependências: `pip install -r requirements.txt`
4. Configure seu `.env` com a `MONGO_URI` e `JWT_SECRET`.
5. Execute a API: `uvicorn app.app:app --reload`

## 🧪 Rodando Testes
```bash
pytest -v
>>>>>>> 8d3e37d (feat: complete saas boilerplate with auth, task-category relationship and 9 passing tests)
```
---

Desenvolvido com ☕ e foco em excelência técnica.
=======
