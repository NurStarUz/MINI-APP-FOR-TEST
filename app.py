import json
import random
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Testlarni yuklash va tasodifiylashtirish
def load_tests():
    with open("tests.json", "r", encoding="utf-8") as file:
        tests = json.load(file)
    return tests

# Testlarni 10ta bo‘limlarga ajratish
def get_test_section(start_index):
    tests = load_tests()
    section = tests[start_index:start_index+10]
    random.shuffle(section)
    return section

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test_sections")
def test_sections():
    total_tests = len(load_tests())
    sections = [(i, i+9) for i in range(0, total_tests, 10)]
    return render_template("test_sections.html", sections=sections)

@app.route("/get_tests/<int:section>")
def get_tests(section):
    tests = get_test_section(section * 10)
    session['current_tests'] = tests
    session['current_index'] = 0
    return render_template("test_section.html", tests=tests, section=section)

@app.route("/start_full_test")
def start_full_test():
    tests = load_tests()
    random.shuffle(tests)
    session['current_tests'] = tests[:100]  # 100 ta test olish
    session['current_index'] = 0
    return render_template("test_section.html", tests=session['current_tests'], section="Full Test")

@app.route("/next_question", methods=["POST"])
def next_question():
    if "current_tests" not in session:
        return jsonify({"error": "Test topilmadi"})
    
    index = session.get("current_index", 0)
    if index >= len(session["current_tests"]):
        return jsonify({"finished": True})
    
    question = session["current_tests"][index]
    session["current_index"] += 1
    return jsonify({"question": question, "index": index})

@app.route("/results")
def results():
    user_results = session.get("user_results", [])
    total_correct = sum(1 for result in user_results if result["correct"])
    total_tests = len(user_results)
    return render_template("results.html", results=user_results, total_correct=total_correct, total_tests=total_tests)

@app.route("/rating")
def rating():
    with open("ratings.json", "r", encoding="utf-8") as file:
        rankings = json.load(file)
    return render_template("rating.html", rankings=rankings)

@app.route("/check_answer", methods=["POST"])
def check_answer():
    data = request.get_json()
    index = data.get("index")
    user_answer = data.get("user_answer")
    user_name = data.get("user_name")

    if "current_tests" not in session:
        return jsonify({"error": "Test topilmadi"})
    
    question = session["current_tests"][index]
    correct_answer = question["togri"]
    is_correct = (user_answer == correct_answer)
    
    user_results = session.get("user_results", [])
    user_results.append({"question": question["savol"], "correct": is_correct})
    session["user_results"] = user_results
    
    # Reytingni yangilash
    with open("ratings.json", "r", encoding="utf-8") as file:
        rankings = json.load(file)
    
    user_entry = next((entry for entry in rankings if entry["name"] == user_name), None)
    if user_entry:
        user_entry["score"] += 1 if is_correct else 0
    else:
        rankings.append({"name": user_name, "score": 1 if is_correct else 0})
    
    with open("ratings.json", "w", encoding="utf-8") as file:
        json.dump(rankings, file, ensure_ascii=False, indent=4)
    
    return jsonify({"result": is_correct, "correct_answer": correct_answer, "delay": 3})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
