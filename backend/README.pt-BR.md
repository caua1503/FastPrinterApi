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
    core/             # Componentes centrais: segurança, agendamento de tarefas (APScheduler)
    helpers/          # Módulos de suporte (ex: conexão com Redis, utilitários)
    models/           # Modelos de dados do ORM (SQLAlchemy)
    routers/api/      # Endpoints da API, organizados por recurso
    schemas/          # Schemas de validação de dados (Pydantic)
    services/         # Lógica de negócio, desacoplada dos endpoints
    scheduler_main.py # Ponto de entrada do serviço de agendamento (APScheduler 3.x)
  migrations/         # Migrações do banco de dados principal (Alembic)

  test/               # Testes automatizados (Pytest)
  compose.yaml        # Orquestração dos serviços com Docker
  create_env.py       # Script para gerar o arquivo de ambiente .env
  init_db.py          # Script para inicializar o banco de dados com dados padrão
```

## Serviço de Agendamento (APScheduler)

Tarefas agendadas rodam em processo separado através do comando:
```bash
uv run python -m app.scheduler_main
```

- **Fuso horário**: Configurado via `TIMEZONE` no `.env` (padrão: `America/Sao_Paulo`).
- **Jobs agendados**:
  - `update_all_printers_maintenance`: Executado diariamente às 02:00.
  - `clean_refresh_tokens`: Executado no dia 1 de cada mês às 03:00.

## Documentação

📖 Leia o [guia de desenvolvimento](docs/pt-br/guia_dev.md) para entender decisões de arquitetura