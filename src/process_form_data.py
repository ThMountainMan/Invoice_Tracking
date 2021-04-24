from dateutil import parser

""" Parse the HTML Form Data and return an update dictionary """


def process_update_data_Invoice(FormData):
    # Process to Form Data for the Invoice Form
    dUpdate = None
    return dUpdate


def process_update_data_Customer(FormData):
    # Process to Form Data for the Invoice Form
    dUpdate = {'name': FormData.get('name').encode('iso-8859-1'),
               'contact': FormData.get('contact').encode('iso-8859-1'),
               'email': FormData.get('email').encode('iso-8859-1'),
               'phone': FormData.get('phone'),
               'street': FormData.get('street').encode('iso-8859-1'),
               'postcode': FormData.get('postcode'),
               'city': FormData.get('city').encode('iso-8859-1'),
               'country': FormData.get('country').encode('iso-8859-1')}
    return dUpdate


def process_update_data_Jobtype(FormData):
    # Process to Form Data for the Jobtype Form
    dUpdate = {'name': FormData.get('name').encode('iso-8859-1')}
    return dUpdate


def process_update_data_Agency(FormData):
    # Process to Form Data for the Agency Form
    dUpdate = {'name': FormData.get('name').encode('iso-8859-1'),
               'percentage': FormData.get('percentage')}
    return dUpdate


def process_update_data_Expense(FormData):
    # Process to Form Data for the Expense Form
    dUpdate = {'expense_id': FormData.get('id'),
               'date': parser.parse(FormData.get('date')),
               'cost': FormData.get('cost'),
               'comment': FormData.get('comment').encode('iso-8859-1')}
    return dUpdate


def process_update_data_PersonalData(FormData):
    # Process to Form Data for the Personal Data Form
    dUpdate = {'label': FormData.get('label').encode('iso-8859-1'),
               'name_company': FormData.get('name_company').encode('iso-8859-1'),
               'name': FormData.get('name').encode('iso-8859-1'),
               'street': FormData.get('street').encode('iso-8859-1'),
               'postcode': FormData.get('postcode'),
               'city': FormData.get('city').encode('iso-8859-1'),
               'mail': FormData.get('mail').encode('iso-8859-1'),
               'phone': FormData.get('phone'),
               'payment_id': FormData.get('payment_details'),
               'taxnumber': FormData.get('taxnumber')
               }
    return dUpdate


def process_update_data_PaymentDetails(FormData):
    # Process to Form Data for the Invoice Form
    dUpdate = {'label': FormData.get('label').encode('iso-8859-1'),
               'name': FormData.get('name').encode('iso-8859-1'),
               'bank': FormData.get('bank').encode('iso-8859-1'),
               'IBAN': FormData.get('IBAN'),
               'BIC': FormData.get('BIC'),
               }
    return dUpdate
