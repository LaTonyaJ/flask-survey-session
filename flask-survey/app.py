from flask import Flask, request, redirect, session
from flask.templating import render_template
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)


RESPONSES_KEY = "responses"


@app.route('/')
def home_page():
    """Select a survey"""

    return render_template("homepage.html", title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)


@app.route('/begin', methods=['POST'])
def begin_survey():
    """Clear Session and redirect to first question """
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route('/questions/<int:id>')
def show_questions(id):
    """Show questions by index number"""
    responses = session.get(RESPONSES_KEY)

    questions = satisfaction_survey.questions
    question = questions[id]

    return render_template("questions.html", question=question)


@app.route('/answer', methods=['POST'])
def save_answers():
    """Save response and redirect to next question unless survey over then Thank them """
    choice = request.form['choice']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def end_of_survey():
    """End of Survey"""
    return render_template("complete.html")
