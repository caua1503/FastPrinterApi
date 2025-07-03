## Getting Started (for production)

Follow these instructions to set up and run the project in your production environment.

### Prerequisites

- Docker and Docker Compose

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/caua1503/FastPrinterApi.git
    cd FastPrinterApi
    ```

## Running the Application

**Step 1: Build the Docker image:**    

    ```bash
    # In the project root
    docker build --no-cache -t fastprinterapi:latest .
    ```

**Step 2: Start Docker Compose:**    

    ```bash
    # In the project root
    docker compose up -d
    ```    