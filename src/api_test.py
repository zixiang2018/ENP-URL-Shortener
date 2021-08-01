import requests

URL = "http://localhost:5000/api/shorten_url"

def test_shorten_url_check_status_code_equals_200():
     response = requests.post(URL, json = {"original_url": "http://www.google.com"})
     assert response.status_code == 200

def test_shorten_url_check_status_code_equals_400():
     response = requests.post(URL, json = {"original_url": "http://www.google.com"})
     assert response.status_code == 400

def test_shorten_url_check_duplicate_entry_https():
     requests.post(URL, json = {"original_url": "http://www.youtube.com"})
     response = requests.post(URL, json = {"original_url": "https://www.youtube.com"})
     assert response.status_code == 400

def test_shorten_url_check_duplicate_entry_http():
     requests.post(URL, json = {"original_url": "https://www.notion.so"})
     response = requests.post(URL, json = {"original_url": "http://www.notion.so"})
     assert response.status_code == 400