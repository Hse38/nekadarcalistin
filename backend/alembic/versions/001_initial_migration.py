"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2026-01-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create employees table
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('surname', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)

    # Create analyses table
    op.create_table(
        'analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('daily_working_hours', sa.Float(), nullable=False),
        sa.Column('weekly_working_days', sa.Float(), nullable=False),
        sa.Column('annual_leave_total', sa.Float(), nullable=False),
        sa.Column('annual_leave_used', sa.Float(), nullable=False),
        sa.Column('extra_leave_days', sa.Float(), nullable=False),
        sa.Column('holidays_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('attendance_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('theoretical_working_days', sa.Float(), nullable=True),
        sa.Column('actual_working_days', sa.Float(), nullable=True),
        sa.Column('theoretical_working_hours', sa.Float(), nullable=True),
        sa.Column('actual_working_hours', sa.Float(), nullable=True),
        sa.Column('difference_hours', sa.Float(), nullable=True),
        sa.Column('calendar_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analyses_id'), 'analyses', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_analyses_id'), table_name='analyses')
    op.drop_table('analyses')
    op.drop_index(op.f('ix_employees_id'), table_name='employees')
    op.drop_table('employees')
