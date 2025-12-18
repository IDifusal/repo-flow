# Flow RMS Assessment – Recipe API

## Overview

This project is a **small Recipe API** built as part of a technical assessment.  

The application exposes both **REST** and **GraphQL** APIs, backed by the same service layer, and includes a simple **AI-based recipe recommendation** with graceful fallback behavior.

---

## Stack Used

- **Python 3.13**
- **FastAPI** (REST API)
- **Strawberry GraphQL**
- **SQLAlchemy 2.0**
- **SQLite** (local development)
- **pytest**
- **Cursor / Context7 / Claude / AI tools** (used as development assistants)

---

## Architecture & Workflow Process

The development followed an incremental and modular approach:

1. **Foundation**
   - Project bootstrap with FastAPI
   - Virtual environment and dependency management
   - Health check endpoints

2. **Database Layer**
   - SQLAlchemy 2.0 engine and session management
   - SQLite for simplicity and fast local setup
   - Lifecycle handled via FastAPI lifespan

3. **Core Domain**
   - `Recipe` model
   - Repository layer for DB access
   - Service layer containing all business logic

4. **REST API**
   - Endpoints for:
     - Create recipe
     - List recipes
     - Delete recipe
     - AI-based recipe recommendation

5. **AI Recommendation**
   - Implemented via a small AI client abstraction
   - Uses a mock AI client by default
   - Graceful fallback if:
     - No recipes exist
     - AI fails or returns invalid data
   - Focused on **integration and design**, not model training

6. **GraphQL API**
   - Strawberry GraphQL mounted on FastAPI
   - Queries and mutations reuse the **same RecipeService**
   - Enabled fast development without duplicating logic

7. **Testing**
   - REST and GraphQL endpoints fully tested
   - AI layer mocked for deterministic tests
   - Isolated database per test run

AI tools (Cursor / Claude) were used during development to:
- Speed up boilerplate
- Identify improvements
- Suggest edge cases and missing validations

---

## API Features

### REST Endpoints

- `POST /recipes`
- `GET /recipes`
- `DELETE /recipes/{id}`
- `GET /recipes/recommendation`

### GraphQL

- `query recipes`
- `query recommendRecipe`
- `mutation createRecipe`
- `mutation deleteRecipe`

Both APIs rely on the **same service layer**, as required.

---

## Running the App Locally

### 1. Clone the repository
```bash
git clone https://github.com/IDifusal/repo-flow
cd repo-flow
```

### 2. Create and activate virtual environment
```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
uvicorn app.main:app --reload
```

- REST docs: http://127.0.0.1:8000/docs  
- GraphQL playground: http://127.0.0.1:8000/graphql  

### 5. Import Postman Collection ( Optional )
- Import file Recipe_API.postman_collection.json
- Use Postman for test rest/graphql endpoints

---

## Running Tests

```bash
pytest
```

or:

```bash
pytest -q
```

### Test Coverage Includes
- REST CRUD operations
- GraphQL queries and mutations
- AI recommendation (mocked)
- Database isolation per test

All tests pass locally.

---

## Possible Future Improvements

- Improve recommendation service using:
  - Larger datasets
  - User preferences
  - Ranking strategies

- Add authentication and authorization
  - Users and roles


- Database:
  - PostgreSQL support
  - Cache and indexing

---

