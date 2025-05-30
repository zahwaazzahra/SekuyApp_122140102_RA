"""init

Revision ID: 1a41e7bb9051
Revises: 
Create Date: 2025-05-28 15:29:46.110517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a41e7bb9051'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bikes',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('thumbnail', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_bikes'))
    )
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    op.create_table('rentals',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('bike_id', sa.BigInteger(), nullable=False),
    sa.Column('rental_date', sa.Date(), nullable=False),
    sa.Column('duration_days', sa.Integer(), nullable=False),
    sa.Column('total_amount', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('payment_method', sa.String(length=50), nullable=False),
    sa.Column('ticket_id', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['bike_id'], ['bikes.id'], name=op.f('fk_rentals_bike_id_bikes')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_rentals_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_rentals')),
    sa.UniqueConstraint('ticket_id', name=op.f('uq_rentals_ticket_id'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rentals')
    op.drop_table('users')
    op.drop_table('bikes')
    # ### end Alembic commands ###
