# FastPrinterAPI Backend

## Tecnologias Utilizadas (Desenvolvimento)

- Testes automatizados (pytest)
- Linter e padronizador de código (Ruff)
- executor de tarefas complementar (Taskipy)

📖 Leia a documentação para executar no modo de [desenvolvimento](docs/pt-br/desenvolvimento.md)

## Estrutura de Pastas & Responsabilidades

O backend é organizado para garantir modularidade, escalabilidade e fácil manutenção, seguindo uma arquitetura em camadas e separação clara de responsabilidades:

```
backend/
  app/
    config/           # Configurações e variáveis de ambiente (via Pydantic)
    core/             # Componentes centrais: segurança, tarefas em background (Celery), logging
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
```

## Documentação

📖 Leia o [guia de desenvolvimento](docs/pt-br/guia_dev.md) para entender decisões de arquitetura