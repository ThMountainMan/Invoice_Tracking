import pdfkit
import os
from app_config import AppConfig

print(AppConfig.path)


def export_to_pdf(source, InvoiceData):
    config = pdfkit.configuration(
        wkhtmltopdf=AppConfig.pfd_creator)

    ID = InvoiceData.invoice_id
    YEAR = InvoiceData.date.year
    NAME = InvoiceData.personal.name

    FilePath = os.path.join(AppConfig.path, str(YEAR))
    FileName = f"Invoice_{NAME.replace(' ', '_')}__{ID}.pdf"

    if not os.path.exists(FilePath):
        os.mkdir(FilePath)

    FullPath = os.path.join(FilePath, FileName)

    print(FullPath)

    pdfkit.from_url(source, FullPath, configuration=config)
