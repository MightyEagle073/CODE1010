from flask import Flask, request, session
from pyhtml import html, form, input_, head, body, div, h1, h2, h3, p, table, th, tr, td, br, link, a, nav, ul, li, img, button, label, select, option
from general import get_login_data

def add_income():
    if request.form["income_amount"][1] == "$":
        input = request.form["income_amount"][:1]
    else:
        input = request.form["income_amount"]
    try: 
        float(input)
    except:
        print("Amount input is not a number")
        session["error_code"] = 401
        return
    if float(input) < 0:
        print("Amount must not be negative")
        session["error_code"] = 402
        return
    if "income_type" not in request.form:
        type = False
    else:
        type = request.form["income_type"]
    if request.form["income_interval"] == "day":
        amount = float(input)
    elif request.form["income_interval"] == "week":
        amount = float(input)/7
    elif request.form["income_interval"] == "fortnight":
        amount = float(input)/14
    elif request.form["income_interval"] == "month":
        amount = float(input)/30.4375
    elif request.form["income_interval"] == "year":
        amount = float(input)/365.25
    append_list = {
        "description": request.form["income_description"],
        "type": type,
        "amount": amount, 
        "category": request.form["income_category"],
    }
    session["database"][session["login"]]["income"] = [append_list] + session["database"][session["login"]]["income"]
    # Assigns ID to every single entry
    i = 1
    print()
    for dict in session["database"][session["login"]]["income"]:
        dict["id"] = i
        i = i + 1
    session.modified = True
    print("20")

def remove_income_input(input):
    session["database"][session["login"]]["income"].pop(int(input) - 1)
    session.modified = True
    # Assigns ID to every single entry
    i = 1
    for dict in session["database"][session["login"]]["income"]:
        dict["id"] = i
        i = i + 1

def get_table_data():
    if session["database"][session["login"]]["income"] == []:
        table_data = html(
            p("No sources of income found in your database. Click the add button to add one!")
        )
    else:
        table_data = [tr(
            th("Description"),
            th("Income Type"),
            th("Amount/Day"),
            th("Amount/Week"),
            th("Amount/Fortnight"),
            th("Amount/Month"),
            th("Amount/Year"),
            th("Category"),
            th("Remove"),
        )]
        if session["database"][session["login"]]["income"] != []:
            for i in range(len(session["database"][session["login"]]["income"])):
                dict = session["database"][session["login"]]["income"][i]
                if dict != {}:
                    if dict["type"] == "":
                        type = "Not Provided"
                    else:
                        type = dict["type"]
                    if dict["category"] == "approx":
                        category = "Approximate"
                    elif dict["category"] == "ats":
                        category = "Exact"
                    table_data = table_data + [tr(
                        td(dict["description"]),
                        td(type),
                        td("$" + "{:,.2f}".format(dict["amount"])),
                        td("$" + "{:,.2f}".format(dict["amount"]*7)),
                        td("$" + "{:,.2f}".format(dict["amount"]*14)),
                        td("$" + "{:,.2f}".format(dict["amount"]*30.4375)),
                        td("$" + "{:,.2f}".format(dict["amount"]*365.25)),
                        td(category),
                        td(
                            form(
                                input_(type = "hidden", name = "income_remove_value", value = str(dict["id"])),
                                input_(type = "submit", name = "income_remove", id = "income_remove", class_ = "income_remove", value = "Remove")
                            )
                        ),   
                    )]
        total = 0
        for dict in session["database"][session["login"]]["income"]:
            total = total + dict["amount"]
        table_data = table_data + [tr(
            td(colspan = 2)("Total"),
            td("$" + "{:,.2f}".format(total)),
            td("$" + "{:,.2f}".format(total * 7)),
            td("$" + "{:,.2f}".format(total * 14)),
            td("$" + "{:,.2f}".format(total * 30.4375)),
            td("$" + "{:,.2f}".format(total * 365.25)),
            td(),
            td(),
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
                th(id = "welcome_heading")("The Income Tracker"),
                th(rowspan = 4)((img(id = "welcome_sheet", src = "static/paycheck.png", alt = "The Income Tracker"))),
            ),
            tr(
                td(id = "welcome_text")("The income tracker keep tracks of your regular income, and how much you earn per day/week/month/year so that you can better manage the decisions you make in your life. It is also great for tracking your income sources so that taxes can be lodged easier when the time comes."),
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
            h1("Your sources of income"),
            button(id = "income_add_income", onClick = "document.getElementById('income_overlay').style.display='block';")("Add"),
            table (id = "income_table")(get_table_data()),
            div(id = "income_overlay", class_ = "overlay")(
                form(
                    div(id = "income_tab", class_ = "tab")(
                        form(
                            h2("Add an income source"),
                            table(id = "income_form_table")(
                                tr(
                                    td(label(for_ = "income_description")("Description:")),
                                    td(input_(type = "text", name = "income_description", id = "income_description", placeholder = "e.g. McDonalds Wage", required = True))
                                ),
                                tr(
                                    td(label(for_ = "income_type")("Income Type:")),
                                    td(input_(type = "text", name = "income_type", id = "income_type", placeholder = "e.g. Wage"))
                                ),
                                tr(
                                    td(label(for_ = "income_amount")("Amount:")),
                                    td(input_(type = "text", name = "income_amount", id = "income_amount", placeholder = "e.g. 303.23", required = True))
                                ),
                                tr(
                                    td(label(for_ = "income_interval")("Interval :")),
                                    td(select(name = "income_interval", id = "income_interval")("Interval")(
                                        option(value = "select")("Select"),
                                        option(value = "day")("Per Day"),
                                        option(value = "week")("Per Week"),
                                        option(value = "fortnight")("Per Fortnight"),
                                        option(value = "month")("Per Month"),
                                        option(value = "year")("Per Year"),
                                    ))
                                ),
                                tr(
                                    td(label(for_ = "income_category")("Category:")),
                                    td(select(name = "income_category", id = "income_category")("Category")(
                                        option(value = "select")("Select"),
                                        option(value = "ats")("Always the same"),
                                        option(value = "approx")("Approximate")
                                    ))
                                ),
                            ),
                            br(),
                            input_(type = "submit", id = "income_add", value = "Add"),
                            button(id = "income_close", onclick = "document.getElementById('income_overlay').style.display='none';")("Cancel"),
                        )
                    ),
                )
            ),
        )

def get_income_html():
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