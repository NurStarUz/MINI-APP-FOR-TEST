from flask import Flask, jsonify, request
import json
import random
import datetime

app = Flask(__name__)

# JSON fayldan testlarni yuklash
def load_tests():
    with open("tests.json", "r", encoding="utf-8") as file:
        return json.load(file)

user_results = []
ranking_data = [
    {"name": "Ali", "score": 8},
    {"name": "Vali", "score": 7},
    {"name": "Sardor", "score": 9},
    {"name": "Madina", "score": 6},
    {"name": "Dilnoza", "score": 10}
]

@app.route('/test', methods=['GET'])
def get_test():
    tests = load_tests()
    random_tests = random.sample(tests, min(10, len(tests)))
    return jsonify(random_tests)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    tests = load_tests()

    index = data.get("index")
    user_answer = data.get("answer")

    if index is None or user_answer is None:
        return jsonify({"error": "Invalid request"}), 400

    correct_answer = tests[index]["togri"]
    is_correct = (user_answer == correct_answer)

    return jsonify({"correct": is_correct, "correct_answer": correct_answer})

@app.route('/results', methods=['GET'])
def get_results():
    return jsonify(user_results)

@app.route('/ranking', methods=['GET'])
def get_ranking():
    sorted_ranking = sorted(ranking_data, key=lambda x: x["score"], reverse=True)[:10]
    return jsonify(sorted_ranking)

@app.route('/submit_result', methods=['POST'])
def submit_result():
    data = request.json
    score = data.get("score", 0)

    user_results.append({
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "score": score
    })
    
    return jsonify({"message": "Natija saqlandi!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
