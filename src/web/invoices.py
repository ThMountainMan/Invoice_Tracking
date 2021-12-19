from bottle import redirect, request, route, static_file, template, get
from database import DbConnection
from dateutil import parser
import export
import logging

log = logging.getLogger(__name__)


# =========================================
# Invoice Related Functions
# =========================================


@route("/")
@get("/invoices")
@get("/invoices/<year>")
def invoices(year=None):
    with DbConnection() as db:
        if year:
            data = [res for res in db.query("invoices") if res.date.year == int(year)]
        else:
            data = db.query("invoices")
        jobtypes = db.query("jobtypes")
        expenses = db.query("expenses")

        # Calculations for the income overview
        income = sum(res.get_ammount()["sum_mwst"] for res in data if res.paydate)
        outstanding = sum(
            res.get_ammount()["sum_mwst"] for res in data if not res.paydate
        )

        expenses = sum(res.cost for res in expenses)
        dOverview = {
            "income": round(income, 2),
            "outstanding": round(outstanding, 2),
            "expenses": round(expenses, 2),
            "profit": round(income - expenses, 2),
        }

    return template("invoicesV2.tpl", overview=dOverview, input=data, jobtypes=jobtypes)


# @route("/invoices/<year>")
# @route("/invoices")
# @route("/")
# def invoices(year=None):
#     # If there is a year specified, get all invoices for this years
#     Data = DB.Invoices.get_all(year)
#     # Get all expenses for the selected year
#     Expenses = DB.Expenses.get_all(year)
#     # Get all available Jobtypes ( for the filter )
#     jobtypes = DB.Jobtypes.get_all()

#     # Calculations for the income overview
#     income = sum(res.get_ammount()["sum_mwst"] for res in Data if res.paydate)
#     outstanding = sum(res.get_ammount()["sum_mwst"] for res in Data if not res.paydate)

#     expenses = sum(res.cost for res in Expenses)
#     dOverview = {
#         "income": round(income, 2),
#         "outstanding": round(outstanding, 2),
#         "expenses": round(expenses, 2),
#         "profit": round(income - expenses, 2),
#     }

#     # Return the template with the defined data
#     return template("invoices.tpl", overview=dOverview, input=Data, jobtypes=jobtypes)


@route("/invoice_show/<id>", method=["POST", "GET"])
def invoice_get(id=None):

    Data = DB.Invoices.get(id)
    log.info(f"Show invoice -{Data.invoice_id}- with id : {id} ...")

    html_data = template(
        "Invoice/Invoice_V1.tpl",
        invoice=Data,
        items=Data.get_items(),
        total=Data.get_ammount()["sum"],
        mwst=Data.get_ammount()["mwst"],
        total_mwst=Data.get_ammount()["sum_mwst"],
    )

    if request.method != "POST":
        return html_data

    File, Path = export.export_to_pdf(html_data, Data)
    return static_file(File, root=Path, download=File)


@route("/invoice_edit/<id>")
@route("/invoice_edit/<id>", method="POST")
def invoice_edit(id=None):
    print("Edit Invoice ...")
    if request.method == "GET" and id:
        # Get the Data for the given invoice
        Data = DB.Invoices.get(id)

        # TODO Enable Editing of Invoices ?!


@route("/invoice_add")
@route("/invoice_add", method="POST")
def invoice_add(id=None):
    print("Add Invoice ...")
    # Check if there is a submitted Form
    if request.method == "POST":
        print("Create Invoice ...")
        # Get the Form Data as Dict
        Data = request.forms

        # Prepare the Data for DB input
        new = DB.Invoices(
            invoice_id=Data.get("id"),
            date=parser.parse(Data.get("date")),
            description=None,
            invoice_mwst=Data.get("mwst"),
            paydate=None,
            # Get all related Data
            customer_id=Data.get("customer_id"),
            jobcode_id=Data.get("jobtype_id"),
            agency_id=Data.get("agency_id"),
            personal_id=Data.get("personal_id"),
        )

        # Create a new Invoice in the DB
        newID = DB.Invoices.create(new)

        # Creat a joint list of the invoice items
        lItems = map(
            list,
            zip(
                request.POST.getall("ammount"),
                request.POST.getall("price"),
                request.POST.getall("comment"),
            ),
        )

        for _item in lItems:
            _new = DB.Invoices_Item(
                parent_id=newID,
                description=_item[2].encode("iso-8859-1"),
                count=_item[0],
                cost=_item[1],
            )
            # Create a new DB entry for the items
            DB.Invoices_Item.create(_new)

        # redirect(f"/invoice_show/{newID}", code=307)
        # redirect(f"/invoice_show/{newID}")
        redirect("/invoices")
    else:
        customers = DB.Customers.get_all()
        agencys = DB.Agencys.get_all()
        jobtypes = DB.Jobtypes.get_all()
        personas = DB.PersonalDetails.get_all()
        newid = DB.Invoices.get_latest_id()
        return template(
            "invoices_edit.tpl",
            id=newid,
            customers=customers,
            agencys=agencys,
            jobtypes=jobtypes,
            personas=personas,
        )


@route("/invoice_delete/<id>")
def invoice_delete(id=None):
    print(f"Deleting Invoice with ID : {id}")
    DB.Invoices.delete(id)
    redirect("/invoices")


@route("/invoice_pay/<id>", method="POST")
def invoice_pay(id=None):
    # We want to edit an existing CUSTOMER
    # So we need to get the data based on the # ID
    # Get the Form Data as Dict
    Data = request.forms
    # Prepare the Data for DB input
    print(Data.get("date"))
    dUpdate = {"paydate": parser.parse(Data.get("date"))}

    DB.Invoices.update(id, dUpdate)
    redirect("/invoices")
