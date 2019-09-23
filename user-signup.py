from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/sign-up')
def display_entry_form():
    return render_template('entry_form.html', title = "Signup", user_name='', user_name_error='', user_password = '', user_password_error='', verify_pswd='', verify_pswd_error='', user_email='', user_email_error='')

def is_wrong(text_value):
    c = ' '
    if len(text_value) < 3 or len(text_value) > 20 or c in text_value:
        return True
    else:
        return False


@app.route('/sign-up', methods=['POST'])
def validate_entry():
    user_name = cgi.escape(request.form['user-name'])
    user_password = request.form['user-password']
    verify_pswd = request.form['verify-pswd']
    user_email = request.form['user-email']

    user_name_error = " "
    user_password_error = " "
    verify_pswd_error = " "
    user_email_error = " "

    special_char = "/!#$}%^&*()+|\{[]"

    if is_wrong(user_name) or user_name == "":
        user_name_error = "Please entre a valid username. Username must be between 3 and 20 characters long and contain no spaces."
        user_name = " "

    if is_wrong(user_password) or user_password == "":
        user_password_error = "Please enter a valid password. Password must be between 3 and 20 characters long and contain no spaces."
        user_password = ""
        verify_pswd = ""

    if user_password_error == " " and user_password != verify_pswd:
        verify_pswd_error = "Passwords do not match"
        user_password = ""
        verify_pswd = ""

    if user_email !="" and not is_wrong(user_email):
        for char in user_email:
            if char in special_char:
                user_email_error = "Please enter a valid email"
                user_email =""

        if user_email_error == " ":
            amp = 0
            dot = 0
            for char in user_email:
                if char == "@":
                    amp +=1
                if char == ".":
                    dot +=1

            if amp != 1 or dot != 1:
                user_email_error = "Please enter a valid email"
                user_email = ""

    if user_name_error == " " and user_password_error == " " and verify_pswd_error == " " and user_email_error == " ":
        return redirect('/welcome?user-name={0}'.format(user_name))
    else:
        return render_template('entry_form.html', title = "Signup", user_name=user_name, user_name_error=user_name_error, user_password=user_password, user_password_error=user_password_error, verify_pswd = verify_pswd, verify_pswd_error = verify_pswd_error, user_email=user_email, user_email_error = user_email_error)

@app.route('/welcome')
def welcome():
    user_name = request.args.get('user-name')
    return '<h1>Welcome, {0}!</h1>'.format(user_name)

app.run()