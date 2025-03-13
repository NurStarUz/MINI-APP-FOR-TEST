from flask import Flask, render_template, request, jsonify, session
import json
import random

app = Flask(__name__)
app.secret_key = "nustar_secret"  # Sessiya uchun

# JSON fayldan testlarni yuklash
def load_tests():
    with open("tests.json", "r", encoding="utf-8") as file:
        return json.load(file)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_test/<int:test_count>")
def start_test(test_count):
    all_tests = load_tests()
    selected_tests = random.sample(all_tests, min(test_count, len(all_tests)))  # Tasodifiy testlar
    session["tests"] = selected_tests
    session["results"] = []
    return render_template("test.html", tests=selected_tests, index=0)

@app.route("/check_answer", methods=["POST"])
def check_answer():
    data = request.json
    index = data["index"]
    user_answer = int(data["user_answer"])

    tests = session.get("tests", [])
    correct_answer = tests[index]["togri"]

    result = {
        "correct": user_answer == correct_answer,
        "correct_answer": correct_answer
    }

    session["results"].append(result)
    
    if index + 1 < len(tests):
        return jsonify({"next_index": index + 1, "result": result})
    else:
        return jsonify({"next_index": None, "result": result})

@app.route("/results")
def results():
    results = session.get("results", [])
    return render_template("results.html", results=results)

@app.route("/rating")
def rating():
    # Bu joyda foydalanuvchi reytingi saqlanadigan baza kerak
    return render_template("rating.html", rankings=[])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
