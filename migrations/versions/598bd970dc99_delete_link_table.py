"""delete link table

Revision ID: 598bd970dc99
Revises: ff99b559701c
Create Date: 2020-04-15 23:04:41.672106

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '598bd970dc99'
down_revision = 'ff99b559701c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('link',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(collation='utf8_bin', length=30), nullable=True),
    sa.Column('url', mysql.VARCHAR(collation='utf8_bin', length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8_bin',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
