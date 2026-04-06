# Binox G3 Deep Research Agent

A powerful, memory-augmented research agent designed to handle complex queries with semantic retrieval and budget constraints.

## Tech Stack
- **Python + FastAPI**: API server and logic layer.
- **OpenAI GPT-4o**: Reasoning engine and query decomposition.
- **ChromaDB**: Persistent vector store for research memory.
- **SQLite (SQLAlchemy)**: Structured log persistence and trace storage.
- **Docker**: Containerized environment.

## Key Features
- **Query Decomposition**: Breaks complex research tasks into 2-4 sub-questions.
- **Memory Management**: Automatically indexes research results and seed documents.
- **Constraint Enforcement**: Tracks token usage and retrieval counts to prevent runaway costs.
- **Self-Evaluation**: Evaluates the quality of its own answers post-synthesis.

## Getting Started

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key

### Local Setup
1. Clone the repository.
2. Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`.
3. Build and run with Docker:
   ```bash
   docker-compose up --build
   ```
4. Access the API at `http://localhost:8000/api/v1/research`.

### Manual Setup
1. Create a virtual environment: `python -m venv venv && source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. (Optional) Index seed docs: `export PYTHONPATH=. && python app/utils/helpers.py`
4. Run the app: `uvicorn app.main:app --reload`

## API Endpoints
- `POST /api/v1/research`: Trigger a research job.
  - Body: `{"query": "Compare AI trends in EU vs US for 2024"}`
- `GET /api/v1/health`: Check system status.

## Evaluation
See [evaluation.md](./evaluation.md) for performance tracking and criteria.
