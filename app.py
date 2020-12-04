from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "HannahMontana"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


debug = DebugToolbarExtension(app)

@app.route("/")
def show_start_survey():
    """Start survey"""
    return render_template("start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear session"""
    session[RESPONSES_KEY] = []

    return redirect("/question/0")
    


@app.route("/question/<int:id>")
def show_question(id):
    """Clear out the response"""
    responses = session.get(RESPONSES_KEY)

    if(responses is None):
        return redirect("/")

    if(len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    if(len(responses) != id):
        flash(f"Invalid question id: {id}.")
        return redirect(f"/question/{len(responses)}")

    """render the questions and question id"""
    question = survey.questions[id]
    return render_template(
        "question.html", question_id=id, question=question)

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/question/{len(responses)}")

@app.route("/complete")
def complete():
    """Survey complete"""
    return render_template("completion.html")