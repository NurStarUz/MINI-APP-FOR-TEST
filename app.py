from flask import Flask, jsonify, render_template, request, session
import json
import random

app = Flask(__name__)
app.secret_key = "nurstar_secret"  # Sessiyalar uchun

def load_questions():
    with open("tests.json", "r", encoding="utf-8") as file:
        return json.load(file)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_tests", methods=["GET"])
def get_tests():
    all_questions = load_questions()
    session["questions"] = random.sample(all_questions, 10)  # 10 ta tasodifiy test
    session["score"] = 0  # Foydalanuvchi natijasi
    session["current_index"] = 0  # Hozirgi test indeksi
    return jsonify(session["questions"])

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.json
    user_answer = data.get("answer")
    index = session.get("current_index", 0)

    questions = session.get("questions", [])
    if index >= len(questions):
        return jsonify({"message": "Barcha testlar tugadi!", "finished": True, "score": session.get("score", 0)})

    correct_answer = questions[index]["variantlar"][questions[index]["togri"]]
    is_correct = (user_answer == correct_answer)

    if is_correct:
        session["score"] += 1  # To‘g‘ri javob uchun ball qo‘shiladi

    session["current_index"] += 1  # Keyingi savolga o‘tish

    return jsonify({
        "correct": correct_answer,
        "is_correct": is_correct,
        "next_question": session["current_index"] < len(questions),
        "score": session["score"]
    })

@app.route("/get_results", methods=["GET"])
def get_results():
    return jsonify({"score": session.get("score", 0)})

@app.route("/get_ranking", methods=["GET"])
def get_ranking():
    return jsonify({"top10": [
        {"name": "Ali", "score": 9},
        {"name": "Hasan", "score": 8},
        {"name": "Olim", "score": 7}
    ]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
