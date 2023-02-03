from flask import Flask, request, session
from pyhtml import html, form, input_, button, head, body, div, h1, h2, h3, p, table, th, tr, td, br, link, a, nav, ul, li, img, label
from general import get_login_data
from datetime import datetime

def change_starting_balance():
    if request.form["starting_balance_input"][1] == "$":
        input = request.form["starting_balance_input"][:1]
    else:
        input = request.form["starting_balance_input"]
    try: 
        float(input)
    except:
        print("Starting balance input is not a number")
        session["error_code"] = 301
        return
    session["database"][session["login"]]["starting_balance"] = float(input)
    session.modified = True
    # Assigns Balance to every single entry
    # if session["database"][session["login"]]["transactions"] != [{}]:
    #     dict = session["database"][session["login"]]["transactions"].pop()
    #     i = len(dict) - 1
    #     dict[i]["balance"] = dict[i]["amount"] + session["database"][session["login"]]["starting_balance"]
    #     while i > 0:
    #         i = i - 1
    #         dict[i]["balance"] = dict[i]["amount"] + dict[i + 1]["balance"]
    #     session["database"][session["login"]]["transactions"] = dict + [{}]
    #     session.modified = True

def add_history_input():
    try:
        (datetime.fromisoformat(request.form["history_form_tt"]))
    except:
        print("Failed to intepret transaction time. Please try another format.")
        session["error_code"] = 302
    if request.form["history_form_amount"][1] == "$":
        input = request.form["history_form_amount"][:1]
    else:
        input = request.form["history_form_amount"]
    try: 
        float(input)
    except:
        print("Amount input is not a number")
        session["error_code"] = 303
        return
    if "history_form_pr" not in request.form:
        pr = False
    else:
        pr = request.form["history_form_pr"]
    if "history_form_location" not in request.form:
        location = False
    else:
        location = request.form["history_form_method"]
    if "history_form_method" not in request.form:
        method = False
    else:
        method = request.form["history_form_method"]
    append_list = {
        "tt": (datetime.fromisoformat(request.form["history_form_tt"]) - datetime(1970, 1, 1)).total_seconds(),
        "description": request.form["history_form_description"],
        "category": request.form["history_form_category"],
        "pr": pr,
        "location": location,
        "method": method,
        "amount": float(input),
    }
    # Appends into already existing database
    print(append_list, "Monki")
    session["database"][session["login"]]["transactions"] = [append_list] + session["database"][session["login"]]["transactions"]
    # if len(session["database"][session["login"]]["transactions"][1]) == {}:
    #     session["database"][session["login"]]["transactions"].pop()
    # Sorts 
    session["database"][session["login"]]["transactions"] = sorted(session["database"][session["login"]]["transactions"], key=lambda transaction: transaction['tt'], reverse=True)
    print()
    # Assigns ID to every single entry
    i = 1
    for dict in session["database"][session["login"]]["transactions"]:
        dict["id"] = i
        i = i + 1
    session.modified = True
    # Assigns Balance to every single entry
    # if session["database"][session["login"]]["transactions"] != [{}]:
    #     dict = session["database"][session["login"]]["transactions"].pop()
    #     i = len(dict) - 1
    #     dict[i]["balance"] = dict[i]["amount"] + session["database"][session["login"]]["starting_balance"]
    #     while i > 0:
    #         i = i - 1
    #         dict[i]["balance"] = dict[i]["amount"] + dict[i + 1]["balance"]
    #     session["database"][session["login"]]["transactions"] = dict + [{}]
    #     session.modified = True
    # # Readds final entry into transactions
    # session["database"][session["login"]]["transactions"] = session["database"][session["login"]]["transactions"] + [{}]
    # session.modified = True

def remove_history_input(input):
    print(input)
    session["database"][session["login"]]["transactions"].pop(int(input) - 1)
    session.modified = True
    # Assigns ID to every single entry
    i = 1
    for dict in session["database"][session["login"]]["transactions"]:
        dict["id"] = i
        i = i + 1
    # Assigns Balance to every single entry
    # if session["database"][session["login"]]["transactions"] != [{}]:
    #     dict = session["database"][session["login"]]["transactions"].pop()
    #     i = len(dict) - 1
    #     dict[i]["balance"] = dict[i]["amount"] + session["database"][session["login"]]["starting_balance"]
    #     while i > 0:
    #         i = i - 1
    #         dict[i]["balance"] = dict[i]["amount"] + dict[i + 1]["balance"]
    #     session["database"][session["login"]]["transactions"] = dict + [{}]
    #     session.modified = True
    session.modified = True

def get_table_data():
    table_data = [tr(
        th("Transaction Time"),
        th("Description"),
        th("Category"),
        th("Payer/Recipient"),
        th("Location"),
        th("Payment Method"),
        th("Amount"),
        th("Balance"),
        th("Remove"),
    )]
    if session["database"][session["login"]]["transactions"] != [{}]:
        for i in range(len(session["database"][session["login"]]["transactions"])):
            dict = session["database"][session["login"]]["transactions"][i]
            if dict != {}:
                if dict["pr"] == "":
                    pr = "Not Provided"
                else:
                    pr = dict["pr"]
                if dict["location"] == "":
                    location = "Not Provided"
                else:
                    location = dict["location"]
                if dict["method"] == "":
                    method = "Not Provided"
                else:
                    method = dict["method"] 
                amount = "$" + "{:,.2f}".format(dict["amount"])
                print(dict)
                table_data = table_data + [tr(
                    td(datetime. fromtimestamp((dict["tt"]))),
                    td(dict["description"]),
                    td(dict["category"]),
                    td(pr),
                    td(location),
                    td(method),
                    td(amount),
                    td("balance"),
                    td(
                        form(
                            input_(type = "hidden", name = "history_remove_value", value = str(dict["id"])),
                            input_(type = "submit", name = "history_remove", id = "history_remove", class_ = "history_remove", value = "Remove")
                        )
                    )
            )]     
    print(session["database"][session["login"]]["starting_balance"])
    starting_balance = "{:,.2f}".format(session["database"][session["login"]]["starting_balance"])
    table_data = table_data + [tr(
        td(colspan = 7)("Starting Balance"),
        td(f"${starting_balance}"),
        td(button(id = "starting_balance_edit_button", onclick = "document.getElementById('starting_balance_overlay').style.display='block';")("Edit")),
    )]
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
                form(
                    div(id = "history_tab", class_ = "tab")(
                        form(
                            h2("Add a transaction"),
                            table(id = "history_form_table")(
                                tr(
                                    td(label(for_ = "history_form_tt")("Transaction Time:")),
                                    td(input_(type = "datetime-local", name = "history_form_tt", id = "history_form_tt", placeholder = "e.g. 24/07/2022 15:31", required = True))
                                ),
                                tr(
                                    td(label(for_ = "history_form_description")("Description:")),
                                    td(input_(type = "text", name = "history_form_description", id = "history_form_description", placeholder = "e.g. Petrol", required = True))
                                ),
                                tr(
                                    td(label(for_ = "history_form_category")("Category:")),
                                    td(input_(type = "text", name = "history_form_category", id = "history_form_category", placeholder = "e.g. Transportation", required = True))
                                ),
                                tr(
                                    td(label(for_ = "history_form_pr")("Payer/Recipient:")),
                                    td(input_(type = "text", name = "history_form_pr", id = "history_form_pr", placeholder = "e.g. Local Service Station"))
                                ),
                                tr(
                                    td(label(for_ = "history_form_location")("Location:")),
                                    td(input_(type = "text", name = "history_form_location", id = "history_form_location", placeholder = "e.g. Hurstville"))
                                ),
                                tr(
                                    td(label(for_ = "history_form_method")("Paid Using:")),
                                    td(input_(type = "text", name = "history_form_method", id = "history_form_method", placeholder = "e.g. Cash"))
                                ),
                                tr(
                                    td(label(for_ = "history_form_amount")("Amount:")),
                                    td(input_(type = "text", name = "history_form_amount", id = "history_form_amount", placeholder = "e.g. -252.65", required = True))
                                ),
                                tr(
                                    td(),
                                    td(p("Note: For a transaction in which you pay someone, enter a negative amount."))
                                )
                            ),
                            br(),
                            input_(type = "submit", id = "history_form_add", value = "Add"),
                            button(id = "history_form_close", onclick = "document.getElementById('history_overlay').style.display='none';")("Cancel"),
                        )
                    ),
                )
            ),
            div(id = "starting_balance_overlay", class_ = "overlay")(
                div(id = "starting_balance_tab", class_ = "tab")(
                    form(   
                        div(id = "starting_balance_container", class_ = "container")(
                            h2("Edit Starting Balance"),
                            p("Starting balance is the amount of money you had before the first transaction in your history took place."),
                            label(for_ = "starting_balance_input")("$"),
                            input_(type = "text", name = "starting_balance_input", id = "starting_balance_input", placeholder = "e.g. 402.54", required = True),
                        ),
                        input_(type = "submit", id = "starting_balance_edit", value = "Edit"),
                        button(id = "starting_balance_close", onclick = "document.getElementById('starting_balance_overlay').style.display='none';")("Close"),
                    ),
                )   
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