"""empty message

Revision ID: 02e0ed4ef48c
Revises: 2.0
Create Date: 2021-12-26 14:11:02.274114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2.1"
down_revision = "2.0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("invoices", schema=None) as batch_op:

        batch_op.create_foreign_key(
            "fk_invoice_jobtypes_id",
            "jobtypes",
            ["jobcode_id"],
            ["id"],
            ondelete="RESTRICT",
        )
        batch_op.create_foreign_key(
            "fk_invoice_customers_id",
            "customers",
            ["customer_id"],
            ["id"],
            ondelete="RESTRICT",
        )
        batch_op.create_foreign_key(
            "fk_invoice_personal_id",
            "personaldetails",
            ["personal_id"],
            ["id"],
            ondelete="RESTRICT",
        )
        batch_op.create_foreign_key(
            "fk_invoice_agencys_id",
            "agencys",
            ["agency_id"],
            ["id"],
            ondelete="RESTRICT",
        )

    with op.batch_alter_table("personaldetails", schema=None) as batch_op:

        batch_op.create_foreign_key(
            "fk_personal_payment_id",
            "paymentdetails",
            ["payment_id"],
            ["id"],
            ondelete="RESTRICT",
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("personaldetails", schema=None) as batch_op:

        batch_op.create_foreign_key(
            "fk_personal_payment_id", "paymentdetails", ["payment_id"], ["id"]
        )

    with op.batch_alter_table("invoices", schema=None) as batch_op:

        batch_op.create_foreign_key(
            "fk_invoice_jobtypes_id", "jobtypes", ["jobcode_id"], ["id"]
        )
        batch_op.create_foreign_key(
            "fk_invoice_agencys_id", "agencys", ["agency_id"], ["id"]
        )
        batch_op.create_foreign_key(
            "fk_invoice_personal_id", "personaldetails", ["personal_id"], ["id"]
        )
        batch_op.create_foreign_key(
            "fk_invoice_customers_id", "customers", ["customer_id"], ["id"]
        )

    # ### end Alembic commands ###