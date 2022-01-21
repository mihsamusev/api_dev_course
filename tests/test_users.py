from unittest import TestCase

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


class UserTests(TestCase):
    def test_root(self):
        res = client.get("/")
        self.assertDictEqual(res.json(), {"message": "i changed, a lot"})
