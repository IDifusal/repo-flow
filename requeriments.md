## The Challenge

Build a small **Recipe API** using:

- **Python 3.13**
- **FastAPI** (REST)
- **Strawberry GraphQL**
- **SQLAlchemy 2.0**

The application should support:
- Creating recipes
- Listing recipes
- Deleting recipes
- **AI-based recipe recommendation**

The scope is intentionally small. We care more about *how* you implement the solution than about feature volume.

---

## Requirements

### Data Model
A recipe should include at minimum:
- `id`
- `title` (required)
- `description` (optional)
- `created_at`

You may add additional fields (e.g., ingredients, tags) if helpful, but keep the model focused.

---

### APIs

#### REST (FastAPI)
Implement:
- `POST /recipes` – create a recipe
- `GET /recipes` – list recipes
- `DELETE /recipes/{id}` – delete a recipe
- `GET /recipes/recommendation` – **return a recommended recipe using AI**

#### GraphQL (Strawberry)
Implement:
- `query recipes(...)`
- `mutation createRecipe(...)`
- `mutation deleteRecipe(...)`
- `query recommendRecipe(...)` – **AI-based recommendation**

Both REST and GraphQL must rely on the **same service layer**.

---

### AI Recommendation Requirement

Implement a simple **AI-powered recommendation** based on the existing recipes.

Guidelines:
- You may use an LLM (OpenAI, Anthropic, local model, or mocked client)
- The AI should receive existing recipe data as context and return one recommended recipe (or a suggestion if none exist)
- The focus is **integration and design**, not model training
- If external APIs are used, credentials must be configurable (env vars, config files, etc.)
- A fallback or graceful failure behavior is expected

Mocking the AI layer in tests is acceptable.

---

### Database
- Use SQLAlchemy **2.0 style**
- SQLite is acceptable for local use
- PostgreSQL is a plus but not required
- Manage sessions and transactions correctly

---

### Testing
- Use `pytest`
- Include tests for:
 - Creating recipes
 - Listing recipes
 - Deleting recipes
 - AI recommendation endpoint (can be mocked)

---

## What We’re Evaluating

We’re looking for senior-level engineering signals:
- Clean architecture and separation of concerns
- Thoughtful API design
- Sensible database modeling
- AI integration done pragmatically (not over-engineered)
- Code clarity, typing, and test quality
- Ability to make and explain tradeoffs

You can and should use AI tools while building this. We’re evaluating the final result and how well it holds together.

---

## Submission

Please submit:
- A Git repository or zip file containing the solution
- A short README with setup and run instructions
- Tests that run locally
