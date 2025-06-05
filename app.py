# app.py

from flask import Flask, render_template_string, request, redirect
from calculator import Calculator, parse_int

app = Flask(__name__)
calculator = Calculator()

TEMPLATE = """
<h2>Mark Calculator</h2>

<!-- Set current overall WAM/UOC -->
<form method="POST" action="/set_current">
  <b>Set current overall WAM and units of credit (if you want to start from these):</b><br>
  WAM: <input name="current_wam" type="number" step="any">
  Units of Credit: <input name="current_uoc" type="number">
  <button type="submit">Set</button>
  {% if set_current_message %}<span style="color:green;">{{ set_current_message }}</span>{% endif %}
  {% if set_current_error %}<span style="color:red;">{{ set_current_error }}</span>{% endif %}
</form>
{% if calculator.current_wam is not none and calculator.current_uoc is not none %}
  <p style="color:blue;">Current overall WAM: {{ calculator.current_wam }} | UOC: {{ calculator.current_uoc }}</p>
{% endif %}

<br>

<!-- Add normal course/mark/credit -->
<form method="POST" action="/add">
  <b>Add a course and mark (optional—can use overall above):</b><br>
  Course: <input name="course" required>
  Mark: <input name="mark" type="number" required>
  Credits: <input name="credit" type="number" required>
  <button type="submit">Add</button>
  {% if add_error %}<span style="color:red;">{{ add_error }}</span>{% endif %}
</form>

<!-- Predict using list of marks -->
<form method="POST" action="/predict" style="margin-top:16px;">
  <b>Predict WAM (with all listed marks):</b><br>
  Course: <input name="course" required>
  Mark: <input name="mark" type="number" required>
  Credits: <input name="credit" type="number" required>
  <button type="submit">Predict</button>
  {% if predict_error %}<span style="color:red;">{{ predict_error }}</span>{% endif %}
  {% if predicted_wam is not none %}<span style="color:green;">Predicted WAM: {{ predicted_wam }}</span>{% endif %}
</form>

<!-- Predict using current overall WAM and UOC -->
<form method="POST" action="/predict_overall" style="margin-top:16px;">
  <b>Predict WAM (with just your overall WAM and UOC):</b><br>
  Mark: <input name="mark" type="number" required>
  Credits: <input name="credit" type="number" required>
  <button type="submit">Predict from Overall</button>
  {% if predict_overall_error %}<span style="color:red;">{{ predict_overall_error }}</span>{% endif %}
  {% if predicted_overall_wam is not none %}<span style="color:green;">Predicted WAM: {{ predicted_overall_wam }}</span>{% endif %}
</form>

<br>

<h3>Marks</h3>
{% if marks %}
  <ul>
  {% for course, (mark, credit) in marks.items() %}
    <li>{{course}}: Mark {{mark}}, Credit {{credit}}
        <form method="POST" action="/remove" style="display:inline">
          <input type="hidden" name="course" value="{{course}}">
          <button type="submit">Remove</button>
        </form>
    </li>
  {% endfor %}
  </ul>
{% else %}
  <i>No marks entered</i>
{% endif %}

<h3>Current WAM (from all listed marks):</h3>
<p>{{wam}}</p>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(
        TEMPLATE,
        marks=calculator.marks,
        wam=f"{calculator.calculate_wam():.2f}",
        add_error=None,
        predict_error=None,
        predicted_wam=None,
        set_current_message=None,
        set_current_error=None,
        predict_overall_error=None,
        predicted_overall_wam=None,
        calculator=calculator
    )

@app.route("/add", methods=["POST"])
def add():
    course = request.form.get("course", "").strip()
    mark = parse_int(request.form.get("mark", ""), "mark")
    credit = parse_int(request.form.get("credit", ""), "credit")
    add_error = None

    if not course or mark is None or credit is None:
        add_error = "Check your inputs."
    elif not calculator.add_mark(course, mark, credit):
        add_error = f"Mark for course {course} already exists."

    return render_template_string(
        TEMPLATE,
        marks=calculator.marks,
        wam=f"{calculator.calculate_wam():.2f}",
        add_error=add_error,
        predict_error=None,
        predicted_wam=None,
        set_current_message=None,
        set_current_error=None,
        predict_overall_error=None,
        predicted_overall_wam=None,
        calculator=calculator
    )

@app.route("/remove", methods=["POST"])
def remove():
    course = request.form.get("course", "").strip()
    calculator.remove_mark(course)
    return redirect("/")

@app.route("/predict", methods=["POST"])
def predict():
    course = request.form.get("course", "").strip()
    mark = parse_int(request.form.get("mark", ""), "mark")
    credit = parse_int(request.form.get("credit", ""), "credit")
    predict_error = None
    predicted_wam = None

    if not course or mark is None or credit is None:
        predict_error = "Check your inputs."
    else:
        predicted = calculator.predict_marks(course, mark, credit)
        if predicted is None:
            predict_error = f"Mark for course {course} already exists."
        else:
            predicted_wam = f"{predicted:.2f}"

    return render_template_string(
        TEMPLATE,
        marks=calculator.marks,
        wam=f"{calculator.calculate_wam():.2f}",
        add_error=None,
        predict_error=predict_error,
        predicted_wam=predicted_wam,
        set_current_message=None,
        set_current_error=None,
        predict_overall_error=None,
        predicted_overall_wam=None,
        calculator=calculator
    )

@app.route("/set_current", methods=["POST"])
def set_current():
    wam = request.form.get("current_wam", "").strip()
    uoc = request.form.get("current_uoc", "").strip()
    set_current_error = None
    set_current_message = None

    try:
        wam_val = float(wam)
        uoc_val = int(uoc)
    except Exception:
        set_current_error = "Inputs must be numbers."
        wam_val = None
        uoc_val = None

    if wam_val is not None and uoc_val is not None:
        if uoc_val < 0 or wam_val < 0:
            set_current_error = "Must be positive."
        else:
            calculator.set_current_overall(wam_val, uoc_val)
            set_current_message = "Current WAM/UOC set!"
    return render_template_string(
        TEMPLATE,
        marks=calculator.marks,
        wam=f"{calculator.calculate_wam():.2f}",
        add_error=None,
        predict_error=None,
        predicted_wam=None,
        set_current_message=set_current_message,
        set_current_error=set_current_error,
        predict_overall_error=None,
        predicted_overall_wam=None,
        calculator=calculator
    )

@app.route("/predict_overall", methods=["POST"])
def predict_overall():
    mark = parse_int(request.form.get("mark", ""), "mark")
    credit = parse_int(request.form.get("credit", ""), "credit")
    predict_overall_error = None
    predicted_overall_wam = None

    if mark is None or credit is None:
        predict_overall_error = "Check your inputs."
    else:
        predicted = calculator.predict_from_current(mark, credit)
        if predicted is None:
            predict_overall_error = "Set your current WAM and units of credit first."
        else:
            predicted_overall_wam = f"{predicted:.2f}"

    return render_template_string(
        TEMPLATE,
        marks=calculator.marks,
        wam=f"{calculator.calculate_wam():.2f}",
        add_error=None,
        predict_error=None,
        predicted_wam=None,
        set_current_message=None,
        set_current_error=None,
        predict_overall_error=predict_overall_error,
        predicted_overall_wam=predicted_overall_wam,
        calculator=calculator
    )

if __name__ == "__main__":
    app.run(debug=True)