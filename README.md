# Invoice Tracking Tool ( Python )

This Invoice Tracking tool is a small webproject to help with invoices for small freelancing Jobs. This is by far not perfect but it works for my general needs. I will use this Tool to improve some of my prgramming skills regarding Webdesign / Github / Docker / Flask. Therefore the Project will probably change a lot based on my current interests and time to work on it. Feedback of any kind id is highly welcomed! 

If this tool proves usefull for any of you, I would be thankfull for a small comment!

## This Project shall fulfill the following purpose:

- Learning how to use Github
- Create a Tool based on Python to manage / track invoices
  - Create Customers
  - Database Interaction
  - Create Invoice
  - Print / Store Invoice
  - DB Revisioning

## Current Functionality :

### Requirements

Python 3.10

Bootstrap V4.6 is beeing used for the bottle templates
https://github.com/twbs/bootstrap/tree/v4.6.0

Convert HTML to PDF:
https://github.com/wkhtmltopdf/wkhtmltopdf


[Requirements for deployment](requirements/common.txt)

[Requirements for development](requirements/develop.txt)

### Ability of the Database / Weberver

=======

### DB Functionality

- [x] DB Revisioning available with alembic
- [ ] Export the DB in CSV Format

### Create a Python Script with basic functionality

- [x] Create / Edit Invoice
- [x] Create / Edit Customer
- [x] Create / Edit Agency
- [x] Create / Edit Job Type

- [x] Create / Edit Personal Data
- [x] Create / Edit Payment Data

- [x] Create / Edit Users

=======

- [X] Get an overview of the Monthly / Yearly Income
- [x] Track unpaied invoices
- [X] Generate PDF Invoices
- [ ] Export Data to CSV

### Store The Information

The Invoice Information is stored in a local sqllite database.
The functionality can be extended to store the date in a remote DB

### Create a GUI for Interaction

Interaction with the Tool is currently based on a Python Flask Webserver.

- [ ] Create a GUI
- [x] Create a Webinterface

### Create Invoices

In order to visualize the Invoice Data, a HTML template has been added.

- [x] Create a Invoice Template in HTML
- [ ] Allow the selection of different Invoice Templates

### Deployment

To deploy the server we can take advantage of several options. Here you find a selection of currently supported ways to deploy the Server.

Available Options:
- [x] Docker Container
- [x] Python enviroment

## How to Use

This section needs to be defined !
=======
