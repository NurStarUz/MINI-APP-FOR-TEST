import json
import random
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Testlarni yuklash va tasodifiylashtirish
def load_tests():
    with open("tests.json", "r", encoding="utf-8") as file:
        tests = json.load(file)
    random.shuffle(tests)  # Testlarni aralashtirish
    return tests

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_tests")
def get_tests():
    tests = load_tests()
    return jsonify(tests)  # Testlarni JSON shaklida qaytarish

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/rating")
def rating():
    return render_template("rating.html")

@app.route("/check_answer", methods=["POST"])
def check_answer():
    data = request.get_json()
    index = data.get("index")
    user_answer = data.get("user_answer")

    with open("tests.json", "r", encoding="utf-8") as file:
        tests = json.load(file)

    correct_answer = tests[index]["togri"]
    is_correct = (user_answer == correct_answer)

    next_index = index + 1 if index + 1 < len(tests) else None

    return jsonify({"result": {"correct": is_correct, "correct_answer": correct_answer}, "next_index": next_index})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)