# Define how to handle new / existing customers
import database as DB


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

    def GetExistingCustomer(self, id=None):
        """ Get the Existing Customer """
        result = DB.get_customer(filter=id)
        if id:
            self.id = id
            self.name = result['name']
            self.contact = result['contact']
            self.street = result['street']
            self.postcode = result['postcode']
            self.city = result['city']
            self.country = result['country']
        else:
            pass

    def CreateNewCustomer(self):
        """ Create a new Customer """
        # TODO: Needs to be implemented based on DB / CVS implementation
        pass


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

    def GetExistingAgency(self, id=None):
        """ Get the Existing Agency """
        result = DB.get_agency(filter=None)

        self.id = id
        self.name = result['name']
        self.percentage = result['percentage']

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

    def get_invoice(self, id=None):
        result = DB.get_invoice(filter=id)
        self.id = id
        self.date = result['date']
        self.customer = result['customer']
        self.description = result['description']
        self.job_type = result['job_type']
        self.agency = result['agency']
        self.invoice_ammount = result['invoice_ammount']
        self.invoice_mwst = result['invoice_mwst']
        self.paydate = result['paydate']

    def edit_invoice(self):
        pass


class Jobtype(object):
    """Class Holds Information about the Jobtype beeing issued / revised"""

    def __init__(self):
        self.id = None
        self.name = None

    def CheckJobtype(self):
        """ Check if a Jobtype is already existant """
        pass

    def GetExistingJobtype(self, id=None):
        """ Get the Existing Agency """
        result = DB.get_jobtype(filter=id)

        self.id = id
        self.name = result['name']

    def CreateNewJobtype(self):
        """ Create a new Jobtype """
        # TODO: Needs to be implemented based on DB / CVS implementation
        pass
