from flask import Flask, request, session
from pyhtml import html, form, input_, head, body, div, h1, h2, h3, p, table, th, tr, td, br, link, a, nav, ul, li, img
from general import get_login_data
from datetime import datetime

def get_greeting():
    if datetime.now().hour >= 3 and datetime.now().hour < 12:
        return "Good morning, " + session["login"]
    elif datetime.now().hour >= 12 and datetime.now().hour < 18:
        return "Good afternoon, " + session["login"]
    else:
        return "Good evening, " + session["login"]

def get_main_data():
    if session["login"] == False:
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
    else:
        return html(
            h2(id = "overview_greeting")(get_greeting()),
            h1(id = "overview_heading")("Your financial overview:"),
            table(id = "overview_container")(
                tr(
                    td(id = "overview_panel_1")(
                        h2("Your current balance:"),
                        h1("$95,986.24"),
                        p("7 day increase: $1,094.24 (1%)"),
                        p("30 day increase: $5,256.44 (5%)"),
                        p("365 day decrease: -$293.75 (-0.3%)")
                    ),
                    td(id = "overview_panel_2")(
                        h2("Your approximate gain per week:"),
                        h1("$339.52"),
                        p("Approximate spendings per week: $1,060.48"),
                        p("Approximate earnings per week: $1,400.00"),
                        p("Gain ratio: 24.25%")
                    )
                ),
                tr(
                    td(id = "overview_panel_3")(
                        h2("The most you've spent this month:"),
                        h1("Entertainment"),
                        p("Spendings on Entertainment this month: $2,532.57 (25%)"),
                        p("Second place: Transport ($626.44, 7%)"),
                        p("Third place: Food and Drinks ($597.22, 6%)")
                    ),
                    td(id = "overview_panel_4")(
                        h2("Next Bill Due:"),
                        h1("Internet Bill"),
                        h3("24/03/2023 - $65"),
                        p("Water Bill: 27/03/2023 - $50"),
                        p("Electricity Bill: 30/03/2023 - $80")
                    )
                ),
            )
        )


def get_mainpage_html():
    return html(
        head(
            link(rel="shortcut icon", type="image/png", href="/static/logo.png"),
            link(rel='stylesheet', href='static/style.css'),
        ),
        body(
            nav(id="navbar")(
                ul(
                    li(a(href="/")("w")),
                    li(a(href="/history")("History")),
                    li(a(href="/income")("Income")),
                    li(a(href="/spendings")("Spendings")),
                    li(a(href="/login")(get_login_data())),
                )
            ),
            div(class_="main_container")(get_main_data()),
        )
    )