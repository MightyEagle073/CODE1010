from flask import Flask, request, session
from pyhtml import html, form, input_, button, head, body, div, h1, h2, h3, p, table, th, tr, td, br, link, a, nav, ul, li, img
from general import get_login_data

def get_table_data():
    table_data = [tr(
        th("Transaction Time"),
        th("Description"),
        th("Category"),
        th("Payer/Recipient"),
        th("Location"),
        th("Paid Using"),
        th("Amount"),
        th("Balance"),
        th(""),
    )]
    table_data = table_data + [tr(
        td(colspan = 7)("Starting Balance"),
        td("$0.00"),
        td(onclick = "document.getElementById('starting_balance_overlay').style.display='block';")("Edit"),
    )]

    table_data = table_data
    return table_data

def get_main_data():
    if session["login"] == False:
        return html(
        table(id = "welcome_container")(
            tr(
                td(colspan = 2, height = "50px")
            ),
            tr(
                th(id = "welcome_heading")("The History Sheet"),
                th(rowspan = 4)((img(id = "welcome_sheet", src = "static/sheet.png", alt = "History Sheet"))),
            ),
            tr(
                td(id = "welcome_text")("The history sheet keeps track of all of your financial history, including all money that you've earnt and all money that you've spent."),
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
            h1("Your transaction history"),
            button(id = "history_add", onClick = "document.getElementById('history_overlay').style.display='block';")("Add"),
            table (id = "history_table")(get_table_data()),
            div(id = "history_overlay", class_ = "overlay")(
                div(id = "history_tab", class_ = "tab")(
                    div(id = "history_container", class_ = "container")(
                        h2("Add a transaction"),
                    ),
                    button(id = "history_form_add", class_ = "close", onclick = "document.getElementById('history_overlay').style.display='none';")("Add"),
                    button(id = "history_form_close", class_ = "close", onclick = "document.getElementById('history_overlay').style.display='none';")("Cancel"),
                ),
            ),
            div(id = "starting_balance_overlay", class_ = "overlay")(
                div(id = "starting_balance_tab", class_ = "tab")(
                    div(id = "starting_balance_container", class_ = "container")(
                        h2("Edit Starting Balance"),
                    ),
                    button(id = "starting_balance_close", class_ = "close", onclick = "document.getElementById('starting_balance_overlay').style.display='none';")("Close"),
                ),
            ),
        )

def get_history_html():
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