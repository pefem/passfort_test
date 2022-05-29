import unittest
import app
import requests



class FlaskTest(unittest.TestCase):

    def test_get_documents(self):
        resp = requests.get("http://127.0.0.1:5000/documents")
        self.assertEqual(resp.status_code, 200)
    

    def test_get_document_revisions(self):
        # tests the GET request
        resp_one = requests.get("http://127.0.0.1:5000/documents/document_one")
        resp_two = requests.get("http://127.0.0.1:5000/documents/smoke")
        self.assertEqual(resp_one.status_code, 200)
        self.assertEqual(resp_two.status_code, 400)

        # tests the POST request
        initial_list = app.document_list
        resp = requests.post("http://127.0.0.1:5000/documents/document_two")
        if resp.status_code == 200:
            self.assertGreater(len(app.document_list), len(initial_list))
    

    # time format to be entered(00:00:00)
    def test_get_document_at_time(self, time_created="14:00:00", title="document_one"):
        resp = requests.get(f"http://127.0.0.1:5000/documents/{title}/{time_created}")
        self.assertEqual(resp.status_code, 200)


unittest.main()