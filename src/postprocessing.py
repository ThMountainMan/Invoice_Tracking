""" Postprocessing functions """
from datetime import datetime


def pp_invoicedata(_count: list, _price: list, _comment: list):
    """Postprocess the Invoice Data and calculate the total of all included items

    Args:
        _count (list): List containing the count of objects
        _price (list): List containing the price of objects
        _comment (list): List containing the comment of objects

    Returns:
        dict: Dictionary containing all invoice Items
    """

    dInvoiceData = {}
    dInvoiceData['ITEMS'] = {}
    dInvoiceData['TOTAL'] = None
    total = 0

    # Creat a joint List of the Database
    lItems = map(list, zip(_count, _price, _comment))

    for id, item in enumerate(lItems):
        item_count = round(float(item[0]), 2)
        item_price = round(float(item[1]), 2)
        item_comment = item[2]

        _sub = round(item_price * item_count, 2)
        total += _sub

        dInvoiceData['ITEMS'][f"#{id+1}"] = {"count": item_count,
                                             "price": item_price,
                                             "subtotal": _sub,
                                             "comment": item_comment.encode('iso-8859-1')}

    dInvoiceData['TOTAL'] = round(total, 2)
    return dInvoiceData


def get_new_id(id: str = None):
    """This function increments the current  ID if no  ID is present a new  ID will be generated

    Args:
        invoice_id (str): The previous  ID

    Returns:
        str: The new  ID
    """

    if not id:
        return f"{datetime.now().year}-{1:03}"

    # Split the String
    year, id = id.split("-")

    # Check if the Year is still valid
    if int(year) != datetime.now().year:
        # We need to create an ID with a new year
        new_year = datetime.now().year
        # also we probably need to start to count from 1 again
        new_id = 1
    else:
        new_year = year
        # Increment the ID
        new_id = int(id) + 1

    return f"{new_year}-{new_id:03}"


if __name__ == '__main__':

    _count = [1, 2]
    _price = [22, 44]
    _comment = ["This is the first", "this is the second"]

    #lItems = map(list, zip(_count, _price, _comment))

    Result = pp_invoicedata(_count, _price, _comment)

    print(Result['TOTAL'])
    print(Result['ITEMS'])
