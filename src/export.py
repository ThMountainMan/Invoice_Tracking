import pdfkit
import os

if not os.path.exists("./invoices"):
    os.mkdir("./invoices")


def export_to_pdf(source, id):
    config = pdfkit.configuration(
        wkhtmltopdf=r"F:\Development\Projects\Invoice_Tracking\recources\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdfkit.from_url(source, f"./invoices/Invoice_{id}.pdf", configuration=config)
