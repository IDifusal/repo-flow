def graphql(client, query: str, variables: dict | None = None):
    # 🤖 Helper function to execute GraphQL queries
    payload = {"query": query, "variables": variables or {}}
    response = client.post("/graphql", json=payload)
    assert response.status_code == 200
    return response.json()


def test_create_and_list_recipes_graphql(client):
    # 🤖 Create recipe via GraphQL mutation
    result = graphql(
        client,
        """
        mutation Create($title: String!, $description: String) {
          createRecipe(title: $title, description: $description) {
            id
            title
            description
          }
        }
        """,
        {"title": "Cake", "description": "Choco"},
    )

    created = result["data"]["createRecipe"]
    assert created["id"] > 0
    assert created["title"] == "Cake"
    assert created["description"] == "Choco"

    # 🤖 Query all recipes
    result = graphql(
        client,
        """
        query {
          recipes {
            id
            title
          }
        }
        """,
    )

    recipes = result["data"]["recipes"]
    assert len(recipes) == 1
    assert recipes[0]["title"] == "Cake"


def test_delete_recipe_graphql(client):
    # 🤖 Create recipe
    created = graphql(
        client,
        """
        mutation {
          createRecipe(title: "Temp", description: null) {
            id
          }
        }
        """,
    )["data"]["createRecipe"]

    recipe_id = created["id"]

    # 🤖 Delete existing recipe
    result = graphql(
        client,
        """
        mutation Delete($id: Int!) {
          deleteRecipe(recipeId: $id)
        }
        """,
        {"id": recipe_id},
    )
    assert result["data"]["deleteRecipe"] is True

    # 🤖 Deleting again should return false
    result = graphql(
        client,
        """
        mutation Delete($id: Int!) {
          deleteRecipe(recipeId: $id)
        }
        """,
        {"id": recipe_id},
    )
    assert result["data"]["deleteRecipe"] is False


def test_recommend_recipe_graphql_mocked_ai(client, monkeypatch):
    # 🤖 Create sample recipes
    r1 = graphql(
        client,
        """
        mutation {
          createRecipe(title: "First", description: null) { id title }
        }
        """,
    )["data"]["createRecipe"]

    r2 = graphql(
        client,
        """
        mutation {
          createRecipe(title: "Second", description: null) { id title }
        }
        """,
    )["data"]["createRecipe"]

    # 🤖 Fake AI client to force recommendation
    class FakeAI:
        def recommend(self, recipes):
            return r2["id"]

    def fake_get_ai_client():
        return FakeAI()

    # 🤖 Monkeypatch GraphQL AI provider
    import app.api.graphql.schema as graphql_schema_module
    monkeypatch.setattr(graphql_schema_module, "get_ai_client", fake_get_ai_client)

    result = graphql(
        client,
        """
        query {
          recommendRecipe {
            id
            title
          }
        }
        """,
    )

    rec = result["data"]["recommendRecipe"]
    assert rec["id"] == r2["id"]
    assert rec["title"] == "Second"
