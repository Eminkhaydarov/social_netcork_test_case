"""refactor table

Revision ID: b623561a7021
Revises: 77f9154c6010
Create Date: 2023-07-09 19:54:32.853213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b623561a7021'
down_revision = '77f9154c6010'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('post_owner_fkey', 'post', type_='foreignkey')
    op.create_foreign_key(None, 'post', 'user', ['owner'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.create_foreign_key('post_owner_fkey', 'post', 'user', ['owner'], ['id'])
    # ### end Alembic commands ###