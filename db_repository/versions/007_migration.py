from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('role', SMALLINT),
    Column('password_hash', VARCHAR(length=128)),
    Column('about_me', VARCHAR(length=140)),
    Column('last_seen', DATETIME),
    Column('location', VARCHAR(length=64)),
    Column('member_since', DATETIME),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('role_id', Integer),
    Column('password_hash', String(length=128)),
    Column('location', String(length=64)),
    Column('about_me', String(length=140)),
    Column('member_since', DateTime),
    Column('last_seen', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['role'].drop()
    post_meta.tables['user'].columns['role_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['role'].create()
    post_meta.tables['user'].columns['role_id'].drop()
