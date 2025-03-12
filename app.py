from flask import Flask, jsonify, request
import json
import random

app = Flask(__name__)

# JSON faylni yuklash
def load_questions():
    with open("tests.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Test olish uchun API
@app.route("/get_test", methods=["GET"])
def get_test():
    questions = load_questions()
    question = random.choice(questions)  # Tasodifiy savol tanlash
    return jsonify(question)

# Foydalanuvchi javobni tekshirish
@app.route("/check_answer", methods=["POST"])
def check_answer():
    data = request.json
    questions = load_questions()

    question_index = data.get("index")
    user_answer = data.get("answer")

    if question_index is None or user_answer is None:
        return jsonify({"error": "Invalid request"}), 400

    correct_answer = questions[question_index]["togri"]
    is_correct = (user_answer == correct_answer)

    return jsonify({"correct": is_correct, "correct_answer": correct_answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
