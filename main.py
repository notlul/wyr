from flask import Flask, render_template, request, jsonify
from tinydb import TinyDB, Query
import os
import random
app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'questions.json')
db = TinyDB(db_path)
questions = Query()


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/creator")
def creator():
    return render_template("create.html")

@app.route("/getQuestion", methods=["GET"])
def getQuestion():
    data = db.all()
    return jsonify(data[random.randint(0,len(data)-1)])

@app.route("/createQuestion/<name>/<option1>/<option2>", methods=["POST"])
def createQuestion(name, option1, option2):
    question_id = len(db) + 1

    db.insert({
        'id': question_id,
        'name': name, 
        'option1': option1,
        'option2': option2,
        'c1': 0,
        'c2': 0
        })
    return jsonify({"status": "success"}), 200
@app.route("/vote/<int:q_id>/<choice>", methods=["POST"])
def vote(q_id, choice):
    Question = Query()
    item = db.get(Question.id == q_id)
    
    if item:
        if choice == 'c1':
            new_val = item.get('c1', 0) + 1
            db.update({'c1': new_val}, Question.id == q_id)
        else:
            new_val = item.get('c2', 0) + 1
            db.update({'c2': new_val}, Question.id == q_id)
            
        updated_item = db.get(Question.id == q_id)
        return jsonify(updated_item), 200
    
    return jsonify({"error": "Not found"}), 404
if __name__ == "__main__":
    app.run(debug=True)