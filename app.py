from flask import Flask, render_template, jsonify, request, session
import random

app = Flask(__name__)
app.secret_key = "nurstar_test_secret"

# Test savollari JSON faylidan yuklanadi
import json

with open("tests.json", "r", encoding="utf-8") as file:
    all_tests = json.load(file)

# Foydalanuvchilarning natijalari
user_results = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start_test", methods=["POST"])
def start_test():
    session["questions"] = random.sample(all_tests, 10)
    session["current_question"] = 0
    session["correct_answers"] = 0
    return jsonify({"status": "started"})

@app.route("/get_question")
def get_question():
    if "questions" not in session or session["current_question"] >= len(session["questions"]):
        return jsonify({"natija": session.get("correct_answers", 0)})

    q = session["questions"][session["current_question"]]
    return jsonify({
        "index": session["current_question"] + 1,
        "savol": q["savol"],
        "variantlar": q["variantlar"],
        "togri": q["togri"]
    })

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.json
    user_answer = data.get("answer")
    correct_answer = session["questions"][session["current_question"]]["togri"]

    correct_index = session["questions"][session["current_question"]]["variantlar"].index(correct_answer)
    selected_index = session["questions"][session["current_question"]]["variantlar"].index(user_answer)

    is_correct = (user_answer == correct_answer)
    if is_correct:
        session["correct_answers"] += 1

    session["current_question"] += 1

    return jsonify({
        "is_correct": is_correct,
        "correct_index": correct_index,
        "selected_index": selected_index
    })

@app.route("/my_results")
def my_results():
    return jsonify({"natijalar": user_results})

@app.route("/top10")
def top10():
    top_results = sorted(user_results, reverse=True)[:10]
    return jsonify({"top": top_results})

@app.route("/save_result", methods=["POST"])
def save_result():
    data = request.json
    user_results.append(data["score"])
    return jsonify({"status": "saved"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
