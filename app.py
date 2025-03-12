from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Test savollari faylini yuklash
def load_tests():
    with open("tests.json", "r", encoding="utf-8") as file:
        return json.load(file)

# 10 ta tasodifiy test tanlash
def get_random_tests():
    all_tests = load_tests()
    return random.sample(all_tests, 10)

# Global o'zgaruvchi testlarni saqlash uchun
current_tests = []
current_index = 0
correct_answers = 0

@app.route("/")
def index():
    global current_tests, current_index, correct_answers
    current_tests = get_random_tests()
    current_index = 0
    correct_answers = 0
    return render_template("index.html")

@app.route("/get_question", methods=["GET"])
def get_question():
    global current_index
    if current_index < len(current_tests):
        question = current_tests[current_index]
        return jsonify({
            "index": current_index + 1,
            "savol": question["savol"],
            "variantlar": question["variantlar"],
            "togri": question["togri"]
        })
    else:
        return jsonify({"natija": correct_answers})

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    global current_index, correct_answers
    data = request.json
    selected_answer = data.get("javob")
    
    if current_index < len(current_tests):
        correct_answer = current_tests[current_index]["variantlar"][current_tests[current_index]["togri"]]
        is_correct = selected_answer == correct_answer
        if is_correct:
            correct_answers += 1
        current_index += 1
        return jsonify({"correct": is_correct, "correct_answer": correct_answer})
    return jsonify({"error": "All questions answered!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
