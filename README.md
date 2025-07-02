# FastPrinterAPI

Uma API assíncrona desenvolvida em FastAPI para o gerenciamento centralizado de múltiplas impressoras, com foco em estatísticas, previsões e histórico detalhado de manutenção.

Embora o núcleo do projeto seja a API RESTful, ele também irá incluir uma interface gráfica intuitiva para facilitar a interação e o gerenciamento (em breve).

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

## Tecnologias Utilizadas (Produção)

- Python 3.12+
- FastAPI (assíncrono)
- Postgres 17 (Banco de dados)
- Redis 8.0 (Banco de cache)
- Pydantic (validação de dados)
- Celery Python (Executor de tarefas e sistema de filas)
- SQLAlchemy (ORM)
- Alembic (migrações)
- Docker (opcional)


## Tecnologias Utilizadas (Desenvolvimento)

- Testes automatizados (pytest)
- Linter e padronizador de código (Ruff)
- executor de tarefas complementar (Taskipy)

## Arquitetura da Aplicação

A arquitetura do FastPrinterAPI foi projetada para ser modular, escalável e de fácil manutenção, seguindo as melhores práticas de desenvolvimento de APIs com FastAPI. A estrutura de diretórios reflete uma clara separação de responsabilidades:

```
FastPrinterAPi/
  app/
    config/           # Configurações e variáveis de ambiente (via Pydantic)
    core/             # Componentes centrais: segurança, tarefas em background (Celery)
    helpers/          # Módulos de suporte (ex: conexão com Redis, utilitários)
    models/           # Modelos de dados do ORM (SQLAlchemy)
    routers/api/      # Endpoints da API, organizados por recurso
    schemas/          # Schemas de validação de dados (Pydantic)
    services/         # Lógica de negócio, desacoplada dos endpoints
  migrations/         # Migrações do banco de dados principal (Alembic)
  migrations_logs/    # Migrações do banco de dados de logs (Alembic)
  test/               # Testes automatizados (Pytest)
  celery_worker.py    # Definição do worker e agendamento de tarefas (Celery Beat)
  compose.yaml        # Orquestração dos serviços com Docker
  create_env.py       # Script para gerar o arquivo de ambiente .env
  init_db.py          # Script para inicializar o banco de dados com dados padrão
  ...
```
