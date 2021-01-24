# Invoice Tracking Tool ( Python )

This is my Firt Repo and Github Projekt. I will keep a record of my progress. The initial Idea is inspired by wanting to learn to use Github and finding something
usefull that is need in my day to day life. Currently I keep track of my Invoices with an Excel sheet, which work perfectly fine but why not try something new.

## This Project shall fulfill the following purpose:

- Learning how to use Github
- Create a Tool based on Python to manage / track invoices
  - Create Customers
  - Database Interaction
  - Create Invoice
  - Print / Store Invoice

## Current Functionality :

### Requirements

Python 3.9

Bootstrap V4.6 is beeing used for the bottle templates
https://github.com/twbs/bootstrap/tree/v4.6.0

Convert HTML to PDF:
https://github.com/wkhtmltopdf/wkhtmltopdf

[Requirements.txt](recources/requirements.txt)

### Ability of the Database / Weberver
- [x] Create / Edit Invoice
- [x] Create / Edit Customer
- [x] Create / Edit Agency
- [x] Create / Edit Job Type
- [x] Create / Edit Personal Data
- [x] Create / Edit Payment Data
- [ ] Get an overview of the Monthly / Yearly Income
- [x] Track unpaied invoices
- [ ] Generate PDF Invoices
- [ ] Export Data to CSV

### Store The Information

The Information is stored in a local sqllite database.
The functionality can be extended to store the date in a remote DB

- [ ] Store the Data in CSV Format
- [x] Extend the functionality to store the information in MySQL Database

### Create a GUI for Interaction

Interaction with the Tool is based on a Python Bottle Webserver.

- [ ] Create a GUI
- [x] Create a Webinterface

### Create Invoices

In order to visualize the Invoice Data, a HTML template has been added.

- [x] Create a Invoice Template in HTML

### Deployment

Currenty the Bottle server has to be started with the Python Enviroment.

Possible Options :
- Docker Container
- PyInstaller
- ...

## How to Use

This section needs to be defined !
