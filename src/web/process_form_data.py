from dateutil import parser

""" Parse the HTML Form Data and return an update dictionary """


def process_update_data_Invoice(FormData):
    return None


def process_update_data_Customer(FormData):
    return {
        "name": FormData.get("name").encode("iso-8859-1"),
        "contact": FormData.get("contact").encode("iso-8859-1"),
        "email": FormData.get("email").encode("iso-8859-1"),
        "phone": FormData.get("phone"),
        "street": FormData.get("street").encode("iso-8859-1"),
        "postcode": FormData.get("postcode"),
        "city": FormData.get("city").encode("iso-8859-1"),
        "country": FormData.get("country").encode("iso-8859-1"),
    }


def process_update_data_Jobtype(FormData):
    return {"name": FormData.get("name").encode("iso-8859-1")}


def process_update_data_Agency(FormData):
    return {
        "name": FormData.get("name").encode("iso-8859-1"),
        "percentage": FormData.get("percentage"),
    }


def process_update_data_Expense(FormData):
    return {
        "expense_id": FormData.get("id"),
        "date": parser.parse(FormData.get("date")),
        "cost": FormData.get("cost"),
        "comment": FormData.get("comment").encode("iso-8859-1"),
    }


def process_update_data_PersonalData(FormData):
    return {
        "label": FormData.get("label").encode("iso-8859-1"),
        "name_company": FormData.get("name_company").encode("iso-8859-1"),
        "name": FormData.get("name").encode("iso-8859-1"),
        "street": FormData.get("street").encode("iso-8859-1"),
        "postcode": FormData.get("postcode"),
        "city": FormData.get("city").encode("iso-8859-1"),
        "mail": FormData.get("mail").encode("iso-8859-1"),
        "phone": FormData.get("phone"),
        "payment_id": FormData.get("payment_details"),
        "taxnumber": FormData.get("taxnumber"),
    }


def process_update_data_PaymentDetails(FormData):
    return {
        "label": FormData.get("label").encode("iso-8859-1"),
        "name": FormData.get("name").encode("iso-8859-1"),
        "bank": FormData.get("bank").encode("iso-8859-1"),
        "IBAN": FormData.get("IBAN"),
        "BIC": FormData.get("BIC"),
    }
