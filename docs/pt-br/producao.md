## Como Começar (para produção)

Siga estas instruções para configurar e executar o projeto em seu ambiente de produção.

### Pré-requisitos

- Docker e Docker Compose

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/caua1503/FastPrinterApi.git
    cd FastPrinterApi
    ```

## Executando a Aplicação

**Passo 1: Ajustar o projeto para português**
Antes de iniciar os contêineres, você precisa modificar o arquivo `entrypoint.sh` para que popule o banco de dados com dados em português.

Abra o arquivo `entrypoint.sh` e faça as seguintes alterações:

    ```diff
    # ... (outras linhas do arquivo)

    # Initialize database
    log "Initializing database..."

    # Adicione a flag -p para inicializar com dados em português
    uv run --no-dev init_db.py -p

    # ... (outras linhas do arquivo)
    ```
Salve as alterações do `entrypoint.sh`.

**Passo 2: Crie a imagem Docker:**    

    ```bash
    # Na raiz do projeto
    docker build --no-cache -t fastprinterapi:latest .
    ```

**Passo 3: Inicie o Docker Compose:**    

    ```bash
    # Na raiz do projeto
    docker compose up -d
    ```    