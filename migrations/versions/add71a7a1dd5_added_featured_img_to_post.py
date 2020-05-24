"""added featured_img to Post

Revision ID: add71a7a1dd5
Revises: 
Create Date: 2020-05-24 20:51:12.401196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add71a7a1dd5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('featured_img', sa.String(), server_default='/static/img/default-img.png', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'featured_img')
    # ### end Alembic commands ###
