"""empty message

Revision ID: 8e8c9b049477
Revises: f9dbf224121c
Create Date: 2021-04-23 12:20:20.382479

"""
from alembic import op
import sqlalchemy as sa
import json

# revision identifiers, used by Alembic.
revision = '1.1'
down_revision = '1.0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    new_table = op.create_table('invoices_item',
                                sa.Column('id', sa.Integer(), nullable=False),
                                sa.Column('description',
                                          sa.VARCHAR(), nullable=True),
                                sa.Column('count', sa.FLOAT(), nullable=True),
                                sa.Column('cost', sa.FLOAT(), nullable=True),
                                sa.Column('parent_id', sa.Integer(),
                                          nullable=True),
                                sa.ForeignKeyConstraint(
                                    ['parent_id'], ['invoices.id'], ),
                                sa.PrimaryKeyConstraint('id'),
                                mysql_engine='InnoDB'
                                )

    # Migrate existing INvoice Data info to the new Invoice Item table.
    # Request all of the old info.
    conn = op.get_bind()
    res = conn.execute("select id, invoice_data from Invoices")
    results = res.fetchall()

    # Prepare an old_info object to insert into the new farminfo table.
    old_info = [{'invoice_data': json.loads(
        r[1])['ITEMS'], 'invoice_id': r[0]} for r in results]

    new_data = list()
    for invoice in old_info:
        ID = invoice['invoice_id']

        for item in invoice['invoice_data']:
            _storage = dict()

            content = invoice['invoice_data'][item]
            _storage['description'] = content['comment']
            _storage['count'] = content['count']
            _storage['cost'] = content['price']
            _storage['parent_id'] = int(ID)

            new_data.append(_storage)

    # We need to get some Dataprovcessing on the go to change migrate the Data ...

    # Insert old_info into new farminfo table.
    op.bulk_insert(new_table, new_data)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invoices_item')
    # ### end Alembic commands ###