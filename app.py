from flask import Flask, jsonify, request
import json
import random
import os

app = Flask(__name__)

# 📌 JSON fayldan testlarni yuklash
def load_tests():
    with open("tests.json", "r", encoding="utf-8") as file:
        return json.load(file)

# 📌 Natijalarni saqlash uchun fayl
RESULTS_FILE = "results.json"

# 📌 Natijalarni yuklash
def load_results():
    if not os.path.exists(RESULTS_FILE):
        return []
    with open(RESULTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# 📌 Natijalarni saqlash
def save_results(results):
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

# 📌 Testlarni olish (tasodifiy 10 ta)
@app.route("/get_tests", methods=["GET"])
def get_tests():
    tests = load_tests()
    random.shuffle(tests)  # Testlarni aralashtiramiz
    return jsonify(tests[:10])  # Faqat 10 tasini yuboramiz

# 📌 Test natijalarini saqlash
@app.route("/save_result", methods=["POST"])
def save_result():
    data = request.json  # Foydalanuvchi natijalarini olish
    results = load_results()
    results.append(data)
    save_results(results)
    return jsonify({"message": "Natijalar saqlandi!"})

# 📌 Foydalanuvchining natijalari
@app.route("/my_results", methods=["GET"])
def my_results():
    results = load_results()
    return jsonify(results)

# 📌 TOP 10 reyting
@app.route("/top10", methods=["GET"])
def top10():
    results = load_results()
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)  # Ballar bo‘yicha saralash
    return jsonify(sorted_results[:10])  # Faqat TOP 10 natijalar

# 📌 Ilovani ishga tushirish
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render avtomatik port belgilashi uchun
    app.run(host="0.0.0.0", port=port, debug=True)
