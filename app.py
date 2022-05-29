from flask import Flask, request, jsonify
from pathlib import Path
import json
from datetime import datetime


app = Flask(__name__)

data = Path("sample_wiki.json").read_text()
document_list = json.loads(data)


# gets a list of avaiable titles
@app.route("/documents", methods=["GET"])
def get_documents():
    available_titles = []
    if len(document_list) > 0:
        for document in document_list:
            available_titles.append({"title": document["title"]})
        
        unique_titles = list({obj["title"]:obj for obj in available_titles}.values())
        return jsonify(unique_titles), 200
    else:
        return "404 Nothing Found", 404