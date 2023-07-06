"""change post table1

Revision ID: cde94bd9ef3d
Revises: 
Create Date: 2023-07-06 15:31:10.165543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cde94bd9ef3d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_post_reaction_user_id_fkey', 'user_post_reaction', type_='foreignkey')
    op.drop_constraint('user_post_reaction_post_id_fkey', 'user_post_reaction', type_='foreignkey')
    op.create_foreign_key(None, 'user_post_reaction', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'user_post_reaction', 'post', ['post_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_post_reaction', type_='foreignkey')
    op.drop_constraint(None, 'user_post_reaction', type_='foreignkey')
    op.create_foreign_key('user_post_reaction_post_id_fkey', 'user_post_reaction', 'post', ['post_id'], ['id'])
    op.create_foreign_key('user_post_reaction_user_id_fkey', 'user_post_reaction', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###