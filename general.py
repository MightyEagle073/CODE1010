from flask import Flask, request, session
from pyhtml import html, table, tr, th, td, img, a

def get_login_data():
    if session["login"] == False:
        return "Log in/Sign up here"
        # return table(tr(td("Logged in as: user123"))), tr(td((("Not you? Click to log out"))))
    else:
        return session["login"]
    
def get_welcome_data():
    return html(
        table(id = "welcome_container")(
            tr(
                td(colspan = 2, height = "50px")
            ),
            tr(
                th(id = "welcome_heading")("Welcome to Fiman!"),
                th(rowspan = 4)((img(id = "welcome_piggy", src = "static/piggy.png", alt = "Piggy Bank"))),
            ),
            tr(
                td(id = "welcome_text")("Fiman is your personal financial manager, which helps you to manage your money better! Fiman logs all of your transactions, income and spendings, and gives you tips on how to save your money better so that you can live a better tomorrow!"),
            ),
            tr(
                td("Get started today!"),
            ),
            tr(
                td(a(href = "/login")("Click here to sign in/sign up")),
            ),
        ),
    )