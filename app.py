# app.py (your main application file)
from flask import Flask, render_template, request
from recommendation import get_recommendations

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['courseName']
        recommendations = get_recommendations(user_input)
        # Process recommendations and display them
        return render_template('results.html', recommendations=recommendations)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
