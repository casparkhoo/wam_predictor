from flask import Flask, render_template, request, redirect, url_for
from calculator import Calculator, parse_int

app = Flask(__name__)
calculator = Calculator()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/marks", methods=["GET", "POST"])
def marks():
    add_error = None
    predict_error = None
    predicted_wam = None

    if request.method == "POST":
        if "add" in request.form:
            course = request.form.get("course", "").strip()
            mark = parse_int(request.form.get("mark", ""), "mark")
            credit = parse_int(request.form.get("credit", ""), "credit")
            if not course or mark is None or credit is None:
                add_error = "Check your inputs."
            elif not calculator.add_mark(course, mark, credit):
                add_error = f"Mark for course {course} already exists."
        elif "predict" in request.form:
            course = request.form.get("course", "").strip()
            mark = parse_int(request.form.get("mark", ""), "mark")
            credit = parse_int(request.form.get("credit", ""), "credit")
            if not course or mark is None or credit is None:
                predict_error = "Check your inputs."
            else:
                predicted = calculator.predict_marks(course, mark, credit)
                if predicted is None:
                    predict_error = f"Mark for course {course} already exists."
                else:
                    predicted_wam = f"{predicted:.2f}"
        elif "predict_multi" in request.form:
            # Gather up to 3 new courses
            new_courses = []
            for i in range(3):
                cname = request.form.get(f"predict_course{i}", "").strip()
                cmark = parse_int(request.form.get(f"predict_mark{i}", ""), "mark")
                ccredit = parse_int(request.form.get(f"predict_credit{i}", ""), "credit")
                if cname and cmark is not None and ccredit is not None:
                    new_courses.append((cname, cmark, ccredit))
            if not new_courses:
                predict_error = "Enter at least one valid course, mark, and credit."
            else:
                predicted = calculator.predict_multiple_marks(new_courses)
                if predicted is None:
                    predict_error = "One of the courses already exists."
                else:
                    predicted_wam = f"{predicted:.2f}"
        elif "remove" in request.form:
            course = request.form.get("remove", "").strip()
            calculator.remove_mark(course)
            return redirect(url_for("marks"))

    return render_template(
        "marks.html",
        marks=calculator.marks,
        wam=f"{calculator.calculate_wam():.2f}",
        add_error=add_error,
        predict_error=predict_error,
        predicted_wam=predicted_wam
    )

@app.route("/overall", methods=["GET", "POST"])
def overall():
    set_current_message = None
    set_current_error = None
    predict_overall_error = None
    predicted_overall_wam = None

    if request.method == "POST":
        if "set_current" in request.form:
            wam = request.form.get("current_wam", "").strip()
            uoc = request.form.get("current_uoc", "").strip()
            try:
                wam_val = float(wam)
                uoc_val = int(uoc)
                if uoc_val < 0 or wam_val < 0:
                    set_current_error = "Must be positive."
                else:
                    calculator.set_current_overall(wam_val, uoc_val)
                    set_current_message = "Current WAM/UOC set!"
            except Exception:
                set_current_error = "Inputs must be numbers."
        elif "predict_overall" in request.form:
            mark = parse_int(request.form.get("mark", ""), "mark")
            credit = parse_int(request.form.get("credit", ""), "credit")
            if mark is None or credit is None:
                predict_overall_error = "Check your inputs."
            else:
                predicted = calculator.predict_from_current(mark, credit)
                if predicted is None:
                    predict_overall_error = "Set your current WAM and units of credit first."
                else:
                    predicted_overall_wam = f"{predicted:.2f}"
        elif "predict_overall_multi" in request.form:
            # Gather up to 3 new courses
            new_courses = []
            for i in range(3):
                cname = request.form.get(f"overall_predict_course{i}", "").strip()
                cmark = parse_int(request.form.get(f"overall_predict_mark{i}", ""), "mark")
                ccredit = parse_int(request.form.get(f"overall_predict_credit{i}", ""), "credit")
                if cname and cmark is not None and ccredit is not None:
                    new_courses.append((cname, cmark, ccredit))
            if not new_courses:
                predict_overall_error = "Enter at least one valid course, mark, and credit."
            else:
                predicted = calculator.predict_multiple_from_current(new_courses)
                if predicted is None:
                    predict_overall_error = "Set your current WAM and units of credit first."
                else:
                    predicted_overall_wam = f"{predicted:.2f}"

    return render_template(
        "overall.html",
        current_wam=calculator.current_wam,
        current_uoc=calculator.current_uoc,
        set_current_message=set_current_message,
        set_current_error=set_current_error,
        predict_overall_error=predict_overall_error,
        predicted_overall_wam=predicted_overall_wam
    )

if __name__ == "__main__":
    app.run(debug=True)