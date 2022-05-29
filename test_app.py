import unittest
import app
import requests



class FlaskTest(unittest.TestCase):

    def test_get_documents(self):
        resp = requests.get("http://127.0.0.1:5000/documents")
        self.assertEqual(resp.status_code, 200)