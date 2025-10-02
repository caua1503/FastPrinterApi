# FastPrinterAPI

<p align="center">
  <a href="https://www.python.org" target="_blank">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://fastapi.tiangolo.com/" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  </a>
  <a href="https://www.postgresql.org" target="_blank">
    <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  </a>
  <a href="https://redis.io" target="_blank">
    <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  </a>
  <a href="https://www.docker.com/" target="_blank">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  </a>
</p>

O FastPrinterAPI é um sistema para gerenciamento centralizado de múltiplas impressoras, com foco em estatísticas, previsões e histórico detalhado de manutenção. O projeto utiliza uma arquitetura monorepo, contendo backend (API) e frontend (interface gráfica) em um único repositório, facilitando integração e manutenção.

## Objetivo

Facilitar o controle, monitoramento e manutenção de parques de impressoras, fornecendo:
- Estatísticas em tempo real de uso e status
- Previsão de próximas recargas e limpezas
- Histórico completo de manutenções, recargas e eventos
- Gestão de departamentos, suprimentos e usuários

## Principais Funcionalidades

- **Gestão de Impressoras:** Cadastro, atualização, consulta e remoção de impressoras.
- **Histórico de Manutenção:** Registro e consulta de manutenções, recargas e limpezas.
- **Previsão Inteligente:** Cálculo da próxima recarga/limpeza com base no histórico.
- **Departamentos:** Organização de impressoras por setores.
- **Sistema multi-usuários:** Com níveis de controle e permissões de acesso.
- **Autenticação Segura:** Endpoints protegidos para operações sensíveis utilizando JWT.
- **Sistema de APIs:** Sistema de API flexível, permitindo a criação de chaves para uma ou várias funções com diferentes níveis de acesso.
- **Sistema de permissões:** Sistema de permissões flexível (RBAC e ABAC) tanto para usuários quanto para APIs.

## Tecnologias Utilizadas

- Python 3.12+
- FastAPI (assíncrono)
- Postgres 17 (Banco de dados)
- Redis 8.0 (Banco de cache)
- Pydantic (validação de dados)
- Celery Python (Executor de tarefas e sistema de filas)
- SQLAlchemy (ORM)
- Alembic (migrações)
- Docker (opcional)

## Arquitetura da Aplicação

A arquitetura do FastPrinterAPI foi projetada para ser modular, escalável e de fácil manutenção, seguindo as melhores práticas de desenvolvimento de APIs com FastAPI. O projeto utiliza uma estrutura monorepo, onde backend e frontend estão organizados no mesmo repositório, garantindo uma separação clara de responsabilidades e facilitando o desenvolvimento integrado.

A estrutura de diretórios é a seguinte:

```
impressoras/
  backend/    # Backend da API (FastAPI, Celery, PostgreSQL, Redis, etc.)
  frontend/   # Aplicação frontend (interface gráfica, em desenvolvimento)
```

Essa abordagem monorepo permite melhor integração entre backend e frontend, versionamento unificado e gerenciamento facilitado de recursos compartilhados. Cada módulo (backend e frontend) é autocontido, com suas próprias dependências e documentação, mas ambos fazem parte do mesmo projeto para um desenvolvimento e deploy mais ágeis.

---

- Para detalhes do backend, consulte: [backend/README.pt-BR.md](backend/README.pt-BR.md)
- Para detalhes do frontend, consulte: [frontend/README.md](frontend/README.md)
- Para guias completos de desenvolvimento e produção, acesse a pasta [docs/pt-br/](backend/docs/pt-br/)