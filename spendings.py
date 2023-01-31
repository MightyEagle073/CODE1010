from flask import Flask, request, session
from pyhtml import html, form, input_, head, body, div, h1, h2, h3, p, table, th, tr, td, br, link, a, nav, ul, li, img
from general import get_login_data

def get_main_data():
    if session["login"] == False:
        return html(
        table(id = "welcome_container")(
            tr(
                td(colspan = 2, height = "50px")
            ),
            tr(
                th(id = "welcome_heading")("The Spending Tracker"),
                th(rowspan = 4)((img(id = "welcome_regiser", src = "static/register.png", alt = "The Spending Tracker"))),
            ),
            tr(
                td(id = "welcome_text")("The spending tracker tracks everything that you pay for regularly, and gives you your approximate total living cost after all that is said and done. It allows you to better understand how you spend your money, and how you can cut down on the spending."),
            ),
            tr(
                td("To access this, please log in."),
            ),
            tr(
                td(a(href = "/login")("Click here to sign in/sign up")),
            ),
        ),
    )
    else:
        return html(
            "Ayy man"
        )

def get_spendings_html():
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
            div(class_="main_container")(get_main_data()),
        )
    )