from flask import Flask, request, session
from pyhtml import html, form, input_, head, body, div, h1, h2, h3, p, table, th, tr, td, br, link, a, nav, ul, li, img, button, label, select, option
from general import get_login_data

def add_spendings():
    if request.form["spendings_amount"][1] == "$":
        input = request.form["spendings_amount"][:1]
    else:
        input = request.form["spendings_amount"]
    try: 
        float(input)
    except:
        print("Amount input is not a number")
        session["error_code"] = 501
        return
    if float(input) < 0:
        print("Amount must not be negative")
        session["error_code"] = 502
        return
    if "spendings_type" not in request.form:
        type = False
    else:
        type = request.form["spendings_type"]
    if request.form["spendings_interval"] == "day":
        amount = float(input)
    elif request.form["spendings_interval"] == "week":
        amount = float(input)/7
    elif request.form["spendings_interval"] == "fortnight":
        amount = float(input)/14
    elif request.form["spendings_interval"] == "month":
        amount = float(input)/30.4375
    elif request.form["spendings_interval"] == "year":
        amount = float(input)/365.25
    append_list = {
        "description": request.form["spendings_description"],
        "type": type,
        "amount": amount, 
        "category": request.form["spendings_category"],
    }
    session["database"][session["login"]]["spendings"] = [append_list] + session["database"][session["login"]]["spendings"]
    # Assigns ID to every single entry
    i = 1
    print()
    for dict in session["database"][session["login"]]["spendings"]:
        dict["id"] = i
        i = i + 1
    session.modified = True
    print("20")

def remove_spendings_input(input):
    session["database"][session["login"]]["spendings"].pop(int(input) - 1)
    session.modified = True
    # Assigns ID to every single entry
    i = 1
    for dict in session["database"][session["login"]]["spendings"]:
        dict["id"] = i
        i = i + 1

def get_table_data():
    if session["database"][session["login"]]["spendings"] == []:
        table_data = html(
            p("No spendings found in the database. Click the add button to add one!")
        )
    else:
        table_data = [tr(
            th("Description"),
            th("Spending Type"),
            th("Amount/Day"),
            th("Amount/Week"),
            th("Amount/Fortnight"),
            th("Amount/Month"),
            th("Amount/Year"),
            th("Category"),
            th("Remove"),
        )]
        if session["database"][session["login"]]["spendings"] != []:
            for i in range(len(session["database"][session["login"]]["spendings"])):
                dict = session["database"][session["login"]]["spendings"][i]
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
                                input_(type = "hidden", name = "spendings_remove_value", value = str(dict["id"])),
                                input_(type = "submit", name = "spendings_remove", id = "spendings_remove", class_ = "spendings_remove", value = "Remove")
                            )
                        ),   
                    )]
        total = 0
        for dict in session["database"][session["login"]]["spendings"]:
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
            h1("Your spendings"),
            button(id = "spendings_add_spending", onClick = "document.getElementById('spendings_overlay').style.display='block';")("Add"),
            table (id = "spendings_table")(get_table_data()),
            div(id = "spendings_overlay", class_ = "overlay")(
                form(
                    div(id = "spendings_tab", class_ = "tab")(
                        form(
                            h2("Add an spendings source"),
                            table(id = "spendings_form_table")(
                                tr(
                                    td(label(for_ = "spendings_description")("Description:")),
                                    td(input_(type = "text", name = "spendings_description", id = "spendings_description", placeholder = "e.g. Rent", required = True))
                                ),
                                tr(
                                    td(label(for_ = "spendings_type")("Spending Type:")),
                                    td(input_(type = "text", name = "spendings_type", id = "spendings_type", placeholder = "e.g. Essentials"))
                                ),
                                tr(
                                    td(label(for_ = "spendings_amount")("Amount:")),
                                    td(input_(type = "text", name = "spendings_amount", id = "spendings_amount", placeholder = "e.g. 902.25", required = True))
                                ),
                                tr(
                                    td(label(for_ = "spendings_interval")("Interval :")),
                                    td(select(name = "spendings_interval", id = "spendings_interval")("Interval")(
                                        option(value = "select")("Select"),
                                        option(value = "day")("Per Day"),
                                        option(value = "week")("Per Week"),
                                        option(value = "fortnight")("Per Fortnight"),
                                        option(value = "month")("Per Month"),
                                        option(value = "year")("Per Year"),
                                    ))
                                ),
                                tr(
                                    td(label(for_ = "spendings_category")("Category:")),
                                    td(select(name = "spendings_category", id = "spendings_category")("Category")(
                                        option(value = "select")("Select"),
                                        option(value = "ats")("Always the same"),
                                        option(value = "approx")("Approximate")
                                    ))
                                ),
                            ),
                            br(),
                            input_(type = "submit", id = "spendings_add", value = "Add"),
                            button(id = "spendings_close", onclick = "document.getElementById('spendings_overlay').style.display='none';")("Cancel"),
                        )
                    ),
                )
            ),
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

    