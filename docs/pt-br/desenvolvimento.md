## Como Começar (para desenvolvimento)

Siga estas instruções para configurar e executar o projeto em seu ambiente de desenvolvimento local.

### Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- `uv` (instalador de pacotes Python)

Este projeto utiliza `uv` para gerenciamento de pacotes e ambientes virtuais. Sua instalação é **obrigatória**.

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/caua1503/FastPrinterApi.git
    cd FastPrinterAPI
    ```

2.  **Crie um ambiente virtual e instale as dependências:**

    ```bash
    # Instale o UV (se ainda não tiver)
    pip install uv
    # ou siga as instruções em: https://docs.astral.sh/uv/getting-started/installation/

    # Crie o ambiente virtual
    uv venv

    # Ative o ambiente virtual
    # Windows
    .venv\Scripts\activate
    # Linux/macOS
    source .venv/bin/activate

    # Instale/sincronize as dependências
    uv sync
    ```

## Executando os Testes

Para garantir a qualidade e a integridade do código, execute a suíte de testes automatizados:

```bash
uv run create_env.py -n
task test
```

Este comando irá formatar o código, verificar por erros de lint e, em seguida, executar os testes com `pytest`.

## Executando a Aplicação

Você pode executar a aplicação de duas formas: com Docker ou localmente.

### 1. Com Docker (Recomendado para Windows)

Esta abordagem é recomendada para desenvolvimento em Windows, pois o Celery (gerenciador de tarefas em segundo plano) possui dependências que não são nativamente compatíveis com este sistema.

**Passo 1: Ajustar o modo de execução para desenvolvimento**

Antes de iniciar os contêineres, você precisa modificar o arquivo `entrypoint.sh` para que a aplicação execute em modo de desenvolvimento (com recarregamento automático) e popule o banco de dados com dados em português.

Abra o arquivo `entrypoint.sh` e faça as seguintes alterações:

```diff
# ... (outras linhas do arquivo)

# Initialize database
log "Initializing database..."

# Adicione a flag -p para inicializar com dados em português
uv run --no-dev init_db.py -p

# ... (outras linhas do arquivo)

# Start FastAPI server
log "Starting FastAPI server..."

# Comente a linha de produção (granian)
# uv run --no-dev granian --interface asgi --host 0.0.0.0 --workers 1 --port 8000 app.main:app

# E descomente a linha de desenvolvimento (fastapi dev)
uv run --no-dev fastapi dev --port 8000 --host 0.0.0.0 --reload ./app
```

**Passo 2: Iniciar os contêineres**

Após salvar as alterações no `entrypoint.sh`, execute o seguinte comando para criar o arquivo `.env`, construir a imagem Docker e iniciar os serviços:

```bash
task windev
```
Os serviços (aplicação, banco de dados, Redis e Celery) estarão rodando em segundo plano. O servidor estará disponível em `http://localhost:8000/docs`.

### 2. Localmente (Apenas Linux/macOS)

Se você estiver em um ambiente Linux ou macOS, pode usar o script de desenvolvimento que automatiza todo o processo.

**Como executar:**

Com o Docker em execução e o ambiente virtual ativado, execute um dos seguintes comandos:

-   **Para inicializar com dados em Português:**
    ```bash
    task dev -p
    ```

**O que o script faz?**

1.  Verifica se o Docker está em execução.
2.  Cria o arquivo `.env` com valores padrão, caso ele não exista.
3.  Inicia os contêineres Docker para os bancos de dados PostgreSQL e para o Redis.
4.  Executa as migrações do banco de dados (schema).
5.  Popula o banco de dados com dados iniciais.
6.  Inicia o servidor FastAPI, o Celery Worker e o Celery Beat.

O servidor estará disponível em `http://127.0.0.1:8000/docs`. Para encerrar todos os processos, basta pressionar `Ctrl+C` no terminal.

