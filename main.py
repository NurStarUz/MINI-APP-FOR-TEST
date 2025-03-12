from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def get_test():
    tests = [
        {"id": 1, "savol": "2 + 2?", "variantlar": ["3", "4", "5"], "togri": "4"},
        {"id": 2, "savol": "3 + 5?", "variantlar": ["7", "8", "9"], "togri": "8"},
    ]
    return jsonify(tests)

@app.route('/results')
def results():
    return jsonify({"message": "Sizning natijalaringiz bu yerda chiqadi"})

@app.route('/ranking')
def ranking():
    return jsonify({"message": "TOP10 reyting"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
