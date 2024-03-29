"""
Export the Data to several ouputs
"""

import logging
import os

import pdfkit

from config import appconfig

log = logging.getLogger(__name__)


def export_to_pdf(source, InvoiceData):

    # check if we are on windows or Linux
    if os.name == "nt":
        config = pdfkit.configuration(wkhtmltopdf=appconfig.pfd_creator)

    ID = InvoiceData.invoice_id
    YEAR = InvoiceData.date.year
    NAME = InvoiceData.personal.name

    FilePath = os.path.join(appconfig.invoice_path, str(YEAR))
    FileName = f"Invoice_{NAME.replace(' ', '_')}__{ID}.pdf"

    log.info(f"Creating Invoice : {FileName} in : {FilePath} ...")

    if not os.path.exists(FilePath):
        os.makedirs(FilePath)

    FullPath = os.path.join(FilePath, FileName)

    if os.name == "nt":
        pdfkit.from_string(source, FullPath, configuration=config)
    else:
        pdfkit.from_string(source, FullPath)

    return [FileName, FilePath]
