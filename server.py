from server import Flask, render_template_string, request, redirect

app = Flask(__name__)
calculator = Calculator()

TEMPLATE = '''
<h2>Mark Calculator</h2>
<form method="POST" action="/add">
  Course: <input name="course" required>
  Mark: <input name="mark" type="number" required>
  Credits: <input name="credit" type="number" required>
  <button type="submit">Add</button>
</form>
<br>
<h3>Marks</h3>
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
<h3>Current WAM:</h3>
<p>{{wam}}</p>
'''

@app.route('/')
def index():
    wam = calculator.calculate_wam()
    return render_template_string(TEMPLATE, marks=calculator.marks, wam=wam)

@app.route('/add', methods=['POST'])
def add():
    course = request.form['course']
    try:
        mark = int(request.form['mark'])
        credit = int(request.form['credit'])
    except ValueError:
        return redirect('/')
    calculator.add_mark(course, mark, credit)
    return redirect('/')

@app.route('/remove', methods=['POST'])
def remove():
    course = request.form['course']
    calculator.remove_mark(course)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)