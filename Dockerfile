FROM python:3.10.0-slim

COPY requirements/common.txt requirements/common.txt
RUN pip install -U pip && pip install -r requirements/common.txt

COPY ./src /app/src
COPY ./bin /app/bin
# COPY ./db/invoice_database.db /app/db/invoice_database.db

WORKDIR /app

# Create a User
RUN useradd demo
# Grant the User Write Permission
RUN chown -R demo:demo /app
RUN chmod 755 /app

# Create the Folder for the DB
RUN mkdir -p /app/db

RUN chown -R demo:demo /app/db
RUN chmod 755 /app/db

# Create the Folder for the Invoices
RUN mkdir -p /app/Invoices

RUN chown -R demo:demo /app/Invoices
RUN chmod 755 /app/Invoices

USER demo 

EXPOSE 8080

ENTRYPOINT ["python", "/app/src/start.py"]