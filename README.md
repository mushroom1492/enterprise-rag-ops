# Enterprise-RAG-Ops: A Production-Grade RAG System with LLMOps and DevOps

## Project Overview

This project demonstrates the development of a production-grade Retrieval-Augmented Generation (RAG) system, meticulously engineered with best practices in LLMOps and DevOps. It showcases a robust approach to building and deploying RAG applications, moving beyond basic scripting to a maintainable, observable, and scalable enterprise solution.

## Core Components and Architecture

### RAG Pipeline (The "Engine")

The RAG pipeline is built using **LangChain** for orchestrating the LLM interactions and retrieval processes. It leverages **ChromaDB** as a persistent vector store for efficient semantic search of document embeddings. **OpenAI's `text-embedding-3-small`** model is used for generating high-quality embeddings, while **OpenAI's `gpt-4o-mini`** serves as the underlying Large Language Model for generating answers. The system supports data ingestion from PDF and Markdown files, utilizing a recursive character splitter for optimal chunking.

### LLMOps (The "Lifecycle")

To ensure the reliability and performance of the RAG system, comprehensive LLMOps practices are integrated:

-   **Evaluation:** **Ragas** is employed for automated evaluation of key RAG metrics, including Faithfulness, Answer Relevance, Context Precision, and Context Recall. This allows for continuous monitoring and improvement of the system's performance.
-   **Observability:** **LangSmith** is utilized for tracing, debugging, and monitoring the RAG pipeline. This provides deep insights into the LLM's behavior and retrieval process, facilitating rapid issue identification and resolution.
-   **Prompt Management:** Prompt templates are versioned and stored in a dedicated module, enabling systematic tracking of prompt changes and their impact on model performance.
-   **Experiment Tracking:** Evaluation metrics are logged, allowing for the tracking of experiments and the comparison of different RAG configurations.

### DevOps (The "Infrastructure")

The project incorporates robust DevOps principles for seamless deployment and operation:

-   **API Layer:** A high-performance **FastAPI** application serves as the API layer, providing endpoints for querying the RAG system and triggering document ingestion.
-   **Containerization:** The entire application is containerized using **Docker** and **Docker Compose**, ensuring portability and consistent environments across development, testing, and production. This includes a multi-container setup for the API and the vector database.
-   **CI/CD:** **GitHub Actions** are configured to automate the Continuous Integration and Continuous Deployment pipeline. This includes automated linting with Ruff, unit testing with Pytest, and Docker image builds upon code pushes and pull requests.
-   **Infrastructure as Code (IaC):** **Terraform** is used to define and provision infrastructure resources (e.g., S3 buckets for document storage, ECR repositories for Docker images), demonstrating cloud-native readiness.
-   **Environment Management:** **Pydantic-Settings** is used for robust and secure management of environment variables and application configuration.

## Project Structure

```
enterprise-rag-ops/
├── .github/
│   └── workflows/          # CI/CD pipelines (GitHub Actions)
├── src/
│   ├── api/                # FastAPI application endpoints
│   ├── core/               # Core RAG logic and LangChain chains
│   ├── eval/               # Ragas evaluation scripts
│   └── utils/              # Configuration, logging, and observability utilities
├── infra/
│   ├── docker/             # Dockerfiles and Docker Compose configurations
│   └── terraform/          # Terraform configurations for IaC
├── tests/                  # Unit and integration tests
├── data/                   # Sample documents for RAG ingestion
├── .env.example            # Template for environment variables
├── Makefile                # Automation commands for common tasks
└── README.md               # Project documentation
```

## Getting Started

### Prerequisites

-   Python 3.11+
-   Docker
-   `pip`
-   An OpenAI API Key
-   (Optional) A LangChain API Key for LangSmith tracing

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/enterprise-rag-ops.git
    cd enterprise-rag-ops
    ```

2.  **Set up environment variables:**
    Create a `.env` file in the root directory based on `.env.example` and fill in your API keys:
    ```bash
    cp .env.example .env
    # Open .env and add your OpenAI and LangChain API keys
    ```

3.  **Install Python dependencies:**
    ```bash
    make install
    ```

### Running the Application

#### Local Development

1.  **Start the FastAPI application:**
    ```bash
    make run
    ```
    The API will be available at `http://127.0.0.1:8000`.

2.  **Ingest documents (if `chroma_db` does not exist or needs update):**
    Place your PDF or Markdown documents in the `data/` directory. Then run:
    ```bash
    make ingest
    ```

3.  **Query the RAG API:**
    You can use `curl` or a tool like Postman/Insomnia to send queries:
    ```bash
    curl -X POST "http://127.0.0.1:8000/query" \
         -H "Content-Type: application/json" \
         -d '{"question": "What is the project about?"}'
    ```

#### Dockerized Deployment

1.  **Build the Docker image:**
    ```bash
    make docker-build
    ```

2.  **Run with Docker Compose:**
    ```bash
    make docker-up
    ```
    The API will be available at `http://localhost:8000`.

### Evaluation

To run the Ragas evaluation (after document ingestion):

```bash
make eval
```

## CI/CD with GitHub Actions

The CI/CD pipeline configuration (originally intended for `.github/workflows/ci.yml`) is provided in `infra/github-workflows/ci.yml`:

-   **Linting:** Uses `ruff` to enforce code style and catch common errors.
-   **Testing:** Runs `pytest` for unit and integration tests.
-   **Docker Build:** Builds the Docker image of the application.

This pipeline is triggered on every push to `main`/`master` and on pull requests.

## Infrastructure as Code with Terraform

The `infra/terraform/main.tf` file provides a basic example of how Terraform can be used to provision cloud resources for this project. In a real-world scenario, this would include:

-   AWS S3 bucket for raw document storage.
-   AWS ECR repository for Docker images.
-   AWS ECS/EKS for container orchestration.
-   Managed database services (e.g., RDS) if ChromaDB were externalized.

## Proficiency Demonstrated

This project showcases proficiency in:

-   **LLMOps:** Implementation of automated RAG evaluation with Ragas, observability with LangSmith, and structured prompt management.
-   **RAG:** Development of a robust RAG pipeline using LangChain, OpenAI embeddings, and ChromaDB, capable of ingesting and querying diverse document types.
-   **DevOps:** Full containerization with Docker, automated CI/CD using GitHub Actions, and foundational Infrastructure as Code with Terraform for cloud deployment readiness.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
