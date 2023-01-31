# Name: Oscar Liang */
# zID: z5363102 */
# Main project file for UNSW CODE1010 23T0 Final Project

from flask import Flask, request, session
from json import dumps
from random import randint
from secrets import token_hex
from mainpage import get_mainpage_html
from login import get_login_html
from history import get_history_html
from income import get_income_html
from spendings import get_spendings_html

APP = Flask(__name__)
APP.config['SECRET_KEY'] = "The quick brown fox jumps over the lazy dog"

@APP.route('/', methods=['GET'])
def mainpage():
    if "initialised" not in session:
        session["initialised"] = True
        session["login"] = False
        session["login_database"] = {}
    return str(get_mainpage_html())

@APP.route('/history', methods=['GET'])
def history():
    if "initialised" not in session:
        print("Return to home")
        return ("no")
    return str(get_history_html())

@APP.route('/income', methods=['GET'])
def income():
    if "initialised" not in session:
        print("Return to home")
        return ("no")
    return str(get_income_html())

@APP.route('/spendings', methods=['GET'])
def spendings():
    if "initialised" not in session:
        print("Return to home")
        return ("no")
    return str(get_spendings_html())

@APP.route('/login', methods=['GET'])
def login():
    if "initialised" not in session:
        print("Return to home")
        return ("no")
    return str(get_login_html())

@APP.route('/debug', methods=['GET'])
def debug():
    if "initialised" not in session:
        print("Return to home")
        return ("no")
    return [
        "session[initialised] : " + str(session["initialised"]),
        "session[login] : " + str(session["login"]),
        "session[login_database] : " + str(session["login_database"]),
    ]

if __name__ == '__main__':
    APP.run(debug=True)