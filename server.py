from flask import Flask, render_template

import data_handler
from data_handler import *

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def home_page():
    all_questions = get_all_user_story()
    return render_template('base.html', all_questions=all_questions)


if __name__ == "__main__":
    app.run(debug=True)
