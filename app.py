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



# returns a list of available revisions
# creates a new version of an exsiting document
@app.route("/documents/<string:title>", methods=["GET", "POST"])
def get_document_revisions(title):

    if request.method == "GET":
        available_revisions = []
        for document in document_list:
            if document["title"] == title:
                available_revisions.append(document)
        else:
            if len(available_revisions) > 0:
                return jsonify(available_revisions)
            else:
                return "no document found", 400
    
    if request.method == "POST":
        available_revisions = []
        for document in document_list:
            if document["title"] == title:
                available_revisions.append(document)
        
        if len(available_revisions) > 1:
            available_revisions.sort(key=lambda doc:doc["version"])

            title_ = title
            version = available_revisions[-1]["version"] + 1
            new_content = request.form["content"]
            time_stamp = datetime.now()
            time = datetime.strftime(time_stamp, "%H:%M:%S")

            new_obj = {
                "title":title_,
                "version": version,
                "content": new_content,
                "time":time
            }
            document_list.append(new_obj)
            print(len(document_list))
            return jsonify(document_list), 201

        elif len(available_revisions) == 1:

            title_ = title
            version = available_revisions[0]["version"] + 1
            new_content = request.form["content"]
            time_stamp = datetime.now()
            time = datetime.strftime(time_stamp, "%H:%M:%S")

            new_obj = {
                "title":title_,
                "version": version,
                "content": new_content,
                "time":time
            }
            document_list.append(new_obj)

            return jsonify(document_list), 201
        
        elif len(available_revisions) == 0:
            return "unable to create item", 400
    

# returns a document as per the provided timestamp
## still a number of cases that can be handled here like if the wrong timestamp is entered
@app.route("/documents/<string:title>/<string:time_created>", methods=["GET"])
def get_document_at_time(title, time_created):
    for document in document_list:
        if document["title"] == title and document["time"] == time_created:
            return jsonify(document), 200
        else:
            return "bad request", 400


# returns the lastest version of a document
@app.route("/documents/<string:title>/latest", methods=["GET"])
def get_latest_document(title):
    available_revisions = []
    for document in document_list:
        if document["title"] == title:
            available_revisions.append(document)
    
    if len(available_revisions) > 1:
        available_revisions.sort(key=lambda doc:doc["version"])
        return jsonify(available_revisions[-1]), 200
    elif len(available_revisions) == 0:
        return "no name with title found", 400
    elif len(available_revisions) == 1:
        return jsonify(available_revisions), 200



    


if __name__ == "__main__":
    app.run(debug=True)