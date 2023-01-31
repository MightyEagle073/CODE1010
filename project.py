# Name: Oscar Liang */
# zID: z5363102 */
# Main project file for UNSW CODE1010 23T0 Final Project

from flask import Flask, request, session, redirect
from json import dumps
from random import randint
from secrets import token_hex
from mainpage import get_mainpage_html
from login import get_login_html, log_in, log_out, create_account, delete_account
from history import get_history_html
from income import get_income_html
from spendings import get_spendings_html

APP = Flask(__name__)
APP.config['SECRET_KEY'] = "The quick brown fox jumps over the lazy dog"

@APP.route('/', methods=['GET'])
def mainpage():
    if "initialised" not in session:
        session["error_code"] = 0
        session["initialised"] = True
        session["login"] = False
        session["database"] = {}
        session.modified = True
    return str(get_mainpage_html())

@APP.route('/history', methods=['GET'])
def history():
    if "initialised" not in session:
        return (redirect("..", code=302))
    return str(get_history_html())

@APP.route('/income', methods=['GET'])
def income():
    if "initialised" not in session:
        return (redirect("..", code=302))
    return str(get_income_html())

@APP.route('/spendings', methods=['GET'])
def spendings():
    if "initialised" not in session:
        return (redirect("..", code=302))
    return str(get_spendings_html())

@APP.route('/login', methods=['POST', 'GET'])
def login():
    if "initialised" not in session:
        return (redirect("..", code=302))
    if request.method == "POST":
        if "login_username" in request.form:
            log_in()
        elif "account_logout" in request.form:
            log_out()
            return (redirect("..", code=302))
        elif "register_username" in request.form:
            create_account()
        elif "account_delete" in request.form:
            delete_account()
            return (redirect("..", code=302))
    return str(get_login_html())

@APP.route('/debug', methods=['GET'])
def debug():
    if "initialised" not in session:
        return (redirect("..", code=302))
    return {
        "initialised": session["initialised"],
        "login": session["login"],
        "database": session["database"],
    }

if __name__ == '__main__':
    APP.run(debug=True)