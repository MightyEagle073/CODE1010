from flask import Flask, request, session, redirect
from pyhtml import html, form, input_, head, body, div, h1, h2, h3, p, table, th, tr, td, br, link, a, nav, ul, li
from general import get_login_data
from datetime import datetime

def get_main_data():
    if session["login"] == False:
        return html(
            form(
                h2("Sign in if you are already registered!"), 
                input_(type = "text", id = "login_username", class_ = "login_inputs", name = "login_username", placeholder = "Username", required = True), 
                br(),
                input_(type = "password", id = "login_password", class_ = "login_inputs", name = "login_password", placeholder = "Password", required = True), 
                br(),
                input_(type = "submit", id = "login_submit", class_ = "login_inputs", name = "login_submit", value = "Sign in"),
            ),
            form(
                h2("Not yet registered? Create an account here!"),
                input_(type = "text", id = "register_username", class_ = "login_inputs", name = "register_username", placeholder = "Choose a Username", required = True), 
                br(),
                input_(type = "password", id = "register_password", class_ = "login_inputs", name = "register_password", placeholder = "Create a Password", required = True), 
                br(),
                input_(type = "password", id = "register_confirm", class_ = "login_inputs", name = "register_confirm", placeholder = "Confirm Password", required = True),
                br(),
                input_(type = "submit", id = "register_submit", class_ = "login_inputs", name = "register_submit", value = "Sign up"),
            )
        )
    else: 
        return html(
            h2(f"Welcome to your account options, {session['login']}!"),
            p(f"Account creation time: {session['database'][session['login']]['created_at']}"),
            form(
                input_(type = "submit", id = "account_logout", class_ = "account_inputs", name = "account_logout", value = "Log Out"),
                input_(type = "submit", id = "account_delete", class_ = "account_inputs", name = "account_delete", value = "Delete Account")
            ),
        )
def log_in():
    if request.form["login_username"] not in session["database"]:
        print("No such user exists in our database!")
        session["error_code"] = 201
    elif request.form["login_password"] != session["database"][request.form["login_username"]]["password"]:
        print("Password Incorrect")
        session["error_code"] = 202
    else:
        session["login"] = request.form["login_username"]
        session.modified = True

def log_out():
    session["login"] = False
    session.modified = True

def create_account():
    if request.form["register_username"] in session["database"]:
        print("Username already taken! Please pick another username.")
        session["error_code"] = 101
    elif len(request.form["register_username"]) < 3:
        print("Username is too short! Usernames must be at least 3 characters long.")
        session["error_code"] = 102
    elif request.form["register_password"] !=  request.form["register_confirm"]:
        print("The password and confirm password fields do not match! Please check your passwords.")
        session["error_code"] = 103
        return
    elif len(request.form["register_password"]) < 8:
        print("Password is too short! Your password must contain at least 8 characters.")
        session["error_code"] = 104
        return
    elif not any(char.isdigit() for char in request.form["register_password"]):
        print("Password must contain at least one number!")
        session["error_code"] = 105
        return
    elif not any(char.isalpha() for char in request.form["register_password"]):
        print("Password must contain at least two letters!")
        session["error_code"] = 106
        return
    elif request.form["register_password"] == request.form["register_password"].lower():
        print("Password must contain at least one uppercase letter!")
        session["error_code"] = 107
        return
    elif request.form["register_password"] == request.form["register_password"].upper():
        print("Password must contain at least one lowercase letter!")
        session["error_code"] = 108
        return
    else:
        print("ok")
        session["database"][request.form["register_username"]] = {
            "password": request.form["register_password"],
            "created_at": datetime.now(),
            "starting_balance": 0.00,
            "transactions": [{}]
        }
        session["login"] = request.form["register_username"]
        session.modified = True
        return

def delete_account():
    print("Account deleted")
    session["database"].pop(session["login"])
    session["login"] = False

def get_login_html():
    return html(
        head( 
            link(rel="shortcut icon", type="image/png", href="/static/logo.png"),
            link(rel='stylesheet', href='static/style.css'),
        ),
        body(
            nav(id="navbar")(
                ul(
                    li(a(href="../")("w")),
                    li(a(href="../history")("History")),
                    li(a(href="../income")("Income")),
                    li(a(href="../spendings")("Spendings")),
                    li(a(href="../login")(get_login_data())),
                )
            ),
            div(class_="main_container")(get_main_data())
        )
    )