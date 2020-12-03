from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "HannahMontana"

debug = DebugToolbarExtension(app)

@app.route("/")
def show_start_survey():
    """Start survey"""
    return render_template("start.html", survey=survey)
    


@app.route("/question/<int:id>")
def show_question(id):
    """render the questions and question id"""
    question = survey.questions[id]
    return render_template(
        "question.html", question_id=id, question=question)

@app.route("/answer", methods=["POST"])
def handle_question():
    choice = request.form['answer']