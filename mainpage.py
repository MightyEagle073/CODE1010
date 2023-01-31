from flask import Flask, request, session
from pyhtml import html, form, input_, head, body, div, h1, h2, h3, p, table, th, tr, td, br, link, a, nav, ul, li, img
from general import get_login_data, get_welcome_data

def get_main_data():
    if True:
        return get_welcome_data()
    else:
        return html()


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