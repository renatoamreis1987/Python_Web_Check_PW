from flask import Flask, render_template, request, redirect

import pw_check

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            pw_to_check = request.form
            checked_pw = pw_check.main(pw_to_check['password'])
            # 1 - return pw_check.main(pw_to_check['password'])
            # return checked_pw_2
            return render_template("checked_pw.html", checked_pw=checked_pw)
        except:
            return 'OK'
    else:
        return 'wrong'
