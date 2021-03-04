"""Teachers relation with faculties and deparementes

Revision ID: 5839c3e629a8
Revises: 61d5bb341d93
Create Date: 2021-03-04 03:36:20.871450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5839c3e629a8'
down_revision = '61d5bb341d93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teachers_departements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('departement_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['departement_id'], ['departements.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teachers_faculties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('faculty_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faculty_id'], ['faculties.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('classrooms', sa.Column('teacher_id', sa.Integer(), nullable=True))
    op.drop_constraint('fk_classroom_owner', 'classrooms', type_='foreignkey')
    op.create_foreign_key('fk_classroom_owner', 'classrooms', 'users', ['teacher_id'], ['id'])
    op.drop_column('classrooms', 'owner_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('classrooms', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint('fk_classroom_owner', 'classrooms', type_='foreignkey')
    op.create_foreign_key('fk_classroom_owner', 'classrooms', 'users', ['owner_id'], ['id'])
    op.drop_column('classrooms', 'teacher_id')
    op.drop_table('teachers_faculties')
    op.drop_table('teachers_departements')
    # ### end Alembic commands ###
