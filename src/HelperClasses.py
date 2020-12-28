# Define how to handle new / existing customers


class Costumer(object):
    """This is a Class to handle The Incoice Custumer
        - Use Existing Custumer
        - Create New Costumer
    """

    def __init__(self):
        self.id = None
        self.name = None
        self.contact = None
        self.street = None
        self.postcode = None
        self.city = None
        self.country = None

    def CheckCustumer(self):
        """ Check if a Customer is already existant """
        pass

    def GetExistingCustomer(self):
        """ Get the Existing Customer """
        # TODO: Needs to be implemented based on DB / CVS implementation
        pass

    def CreateNewCustomer(self):
        """ Create a new Customer """
        # TODO: Needs to be implemented based on DB / CVS implementation
        pass

    def print_out(self):
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Contact: {self.contact}")
        print(f"Street: {self.street}")
        print(f"Postcode: {self.postcode}")
        print(f"City: {self.city}")


class Agency(object):
    """This is a Clas to handle Agencys
        - Use Existing Agency
        - Create New Agency
    """

    def __init__(self):
        self.id = None

        self.name = None
        self.percentage = None

    def CheckAgency(self):
        """ Check if a Agency is already existant """
        pass

    def GetExistingAgency(self):
        """ Get the Existing Agency """
        # TODO: Needs to be implemented based on DB / CVS implementation
        pass

    def CreateNewAgency(self):
        """ Create a new Agency """
        # TODO: Needs to be implemented based on DB / CVS implementation
        pass


class Invoce(object):
    """Class Holds Information about the Invoice beeing issued / revised"""

    def __init__(self):
        self.id = None
        self.date = None
        self.customer = None
        self.description = None
        self.job_type = None
        self.agency = None
        self.invoice_ammount = None
        self.invoice_mwst = None
        self.paydate = None

    def add_invoice(self):
        pass

    def get_invoice(self):
        pass

    def edit_invoice(self):
        pass
