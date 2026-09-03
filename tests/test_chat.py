from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_chat():
    with patch("app.main.generate_response") as mock_generate:
        mock_generate.return_value = "This is a test response."

        response = client.post(
                "/chat",
                json={"prompt": "Hello"}
        )

        assert response.status_code == 200
        assert response.json() == {
                "response": "This is a test response."
        }
        
        mock_generate.assert_called_once_with("Hello")
