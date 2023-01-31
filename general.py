from flask import Flask, request, session
from pyhtml import html, table, tr, th, td, img, a

def get_login_data():
    if session["login"] == False:
        return "Log in/Sign up here"
    else:
        return f"Welcome, {session['login']}!"