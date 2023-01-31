from flask import Flask, request, session
from pyhtml import html, form, input_, head, body, div, h1, h2, h3, p, table, th, tr, td, br, link, a, nav, ul, li
from general import get_login_data

def get_main_data():
    if 20 == 20:
        return html(
            form(
                h2("Sign in if you are already registered!"), 
                input_(type = "text", name = "login_id", class_ = "login_inputs", placeholder = "Username", required = True), 
                br(),
                input_(type = "password", id = "login_password", class_ = "login_inputs", name = "login_password", placeholder = "Password", required = True), 
                br(),
                input_(type = "submit", id = "login_submit", class_ = "login_inputs", name = "login_submit", value = "Sign in"),
            ),
            form(
                h2("Not yet registered? Create an account here!"),
                input_(type = "text", id = "register_id", class_ = "login_inputs", name = "register_id", placeholder = "Choose a Username", required = True), 
                br(),
                input_(type = "password", id = "register_password", class_ = "login_inputs", name = "register_password", placeholder = "Create a Password", required = True), 
                br(),
                input_(type = "password", id = "register_confirm", class_ = "login_inputs", name = "register_confirm", placeholder = "Confirm Password", required = True),
                br(),
                input_(type = "submit", id = "register_submit", class_ = "login_inputs", name = "register_submit", value = "Sign up"),
            )
        )
    else: 
        return

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