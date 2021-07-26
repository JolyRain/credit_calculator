from flask import Flask, render_template, request, redirect
from creditcalc import DiffCalc, AnnCalc, CreditCalc

app = Flask(__name__)

diff_calc = DiffCalc()
ann_calc = AnnCalc()
credit_calc = 0


@app.route('/', methods=['POST', 'GET'])
def index():
    global diff_calc, ann_calc, credit_calc
    if request.method == 'POST':
        loan_sum = int(request.form['loan'])
        rate = float(request.form['rate'])
        period = int(request.form['period'])
        credit_type = request.form['credit_type']
        diff_calc = DiffCalc(loan_sum, period, rate)
        ann_calc = AnnCalc(loan_sum, period, rate)

        if credit_type == 'diff':
            credit_calc = diff_calc
        if credit_type == 'ann':
            credit_calc = ann_calc

        return redirect('/result')
    else:
        return render_template("index.html")


@app.route('/result')
def result():
    return render_template('result.html', credit_calc=credit_calc)


if __name__ == "__main__":
    app.run(debug=True)
