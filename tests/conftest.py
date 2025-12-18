import os
import sys
import importlib
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path):
    # 🤖 Create an isolated SQLite database per test run
    # This avoids test pollution and keeps tests deterministic
    db_path = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    # 🤖 Remove previously loaded app modules
    # This forces Python to reload the app using the new DATABASE_URL
    modules_to_delete = [m for m in sys.modules if m == "app" or m.startswith("app.")]
    for m in modules_to_delete:
        del sys.modules[m]

    # 🤖 Import the FastAPI app AFTER setting env vars
    app_main = importlib.import_module("app.main")

    # 🤖 TestClient triggers FastAPI lifespan events automatically
    # This means tables are created via create_all()
    with TestClient(app_main.app) as test_client:
        yield test_client
