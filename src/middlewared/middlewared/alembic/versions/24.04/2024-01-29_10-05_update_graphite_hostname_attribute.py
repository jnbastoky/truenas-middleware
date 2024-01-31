"""Update graphite hostname attribute

Revision ID: 6a7c2281f48e
Revises: 7c456c2a4926
Create Date: 2024-01-29 10:05:47.440945+00:00

"""
import json

from alembic import op
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = '6a7c2281f48e'
down_revision = '7c456c2a4926'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    for attr in conn.execute('SELECT attributes FROM reporting_exporters').fetchall():
        attributes = json.loads(attr['attributes'])
        attributes['namespace'] = attributes.pop('hostname')
        conn.execute(
            text('UPDATE reporting_exporters set attributes=:attributes'),
            attributes=json.dumps(attributes)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
