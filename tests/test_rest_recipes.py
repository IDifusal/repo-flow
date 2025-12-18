def test_create_recipe_rest(client):
    # 🤖 Create a recipe via REST
    response = client.post("/recipes", json={"title": "Pasta", "description": "Quick"})
    assert response.status_code == 201

    data = response.json()
    assert data["id"] > 0
    assert data["title"] == "Pasta"
    assert data["description"] == "Quick"
    assert "created_at" in data


def test_list_recipes_rest(client):
    # 🤖 Create multiple recipes
    client.post("/recipes", json={"title": "A", "description": None})
    client.post("/recipes", json={"title": "B", "description": "x"})

    # 🤖 Fetch all recipes
    response = client.get("/recipes")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2

    titles = [r["title"] for r in data]
    assert "A" in titles
    assert "B" in titles


def test_delete_recipe_rest(client):
    # 🤖 Create recipe to delete
    created = client.post("/recipes", json={"title": "To delete", "description": None}).json()
    recipe_id = created["id"]

    # 🤖 Delete existing recipe
    response = client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 204

    # 🤖 Deleting again should return 404
    response = client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 404


def test_recommendation_rest_no_recipes(client):
    # 🤖 Recommendation when there are no recipes
    response = client.get("/recipes/recommendation")
    assert response.status_code == 200

    data = response.json()
    assert data["recipe"] is None
    assert isinstance(data["message"], str)


def test_recommendation_rest_with_mocked_ai(client, monkeypatch):
    # 🤖 Create sample recipes
    r1 = client.post("/recipes", json={"title": "First", "description": None}).json()
    r2 = client.post("/recipes", json={"title": "Second", "description": None}).json()

    # 🤖 Fake AI that always recommends the second recipe
    class FakeAI:
        def recommend(self, recipes):
            return r2["id"]

    def fake_get_ai_client():
        return FakeAI()

    # 🤖 Monkeypatch the AI provider to force deterministic behavior
    import app.api.rest.recipes as rest_recipes_module
    monkeypatch.setattr(rest_recipes_module, "get_ai_client", fake_get_ai_client)

    response = client.get("/recipes/recommendation")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] is None
    assert data["recipe"]["id"] == r2["id"]
    assert data["recipe"]["title"] == "Second"
