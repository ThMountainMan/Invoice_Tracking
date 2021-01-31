""" Postprocessing functions """


def pp_invoicedata(_count, _price, _comment):
    """ Get the Items from the Invoice and do some postprocessing """
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
                                             "comment": item_comment}
        #print(f"""NR: {id+1}\nCount: {item_count}\nPrice: {item_price}\nSubTotal: {_sub}\nComment: {item_comment}\n""")

    dInvoiceData['TOTAL'] = round(total, 2)
    return dInvoiceData


if __name__ == '__main__':

    _count = [1, 2]
    _price = [22, 44]
    _comment = ["This is the first", "this is the second"]

    #lItems = map(list, zip(_count, _price, _comment))

    Result = pp_invoicedata(_count, _price, _comment)

    print(Result['TOTAL'])
    print(Result['ITEMS'])
