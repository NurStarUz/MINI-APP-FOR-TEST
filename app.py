from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import random

app = Flask(__name__)
app.secret_key = "nurstar_secret_key"

# Testlarni yuklash
def load_tests():
    with open("tests.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Bosh sahifa
@app.route("/")
def index():
    return render_template("index.html")

# Testni boshlash (10 yoki 50 talik)
@app.route("/start_test/<int:num_questions>")
def start_test(num_questions):
    tests = load_tests()
    session["questions"] = random.sample(tests, num_questions)
    session["current_question"] = 0
    session["correct_answers"] = 0
    return redirect(url_for("test"))

# Test savollarini chiqarish
@app.route("/test", methods=["GET", "POST"])
def test():
    if "questions" not in session or session["current_question"] >= len(session["questions"]):
        return redirect(url_for("results"))

    question_data = session["questions"][session["current_question"]]

    if request.method == "POST":
        selected_option = int(request.form["answer"])
        correct_option = question_data["answer"]

        if selected_option == correct_option:
            session["correct_answers"] += 1
            feedback = "correct"
        else:
            feedback = "incorrect"

        session["current_question"] += 1
        return jsonify({"feedback": feedback, "correct_option": correct_option})

    return render_template("test.html", question=question_data, question_num=session["current_question"] + 1)

# Natijalar
@app.route("/results")
def results():
    score = session.get("correct_answers", 0)
    total = len(session.get("questions", []))
    return render_template("results.html", score=score, total=total)

# API - Testlarni olish
@app.route("/api/tests", methods=["GET"])
def api_tests():
    return jsonify(load_tests())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
