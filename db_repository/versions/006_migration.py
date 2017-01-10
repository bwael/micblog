from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
role = Table('role', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('default', Boolean, default=ColumnDefault(False)),
    Column('permissions', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
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
    post_meta.tables['role'].create()
    post_meta.tables['user'].columns['location'].create()
    post_meta.tables['user'].columns['member_since'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['role'].drop()
    post_meta.tables['user'].columns['location'].drop()
    post_meta.tables['user'].columns['member_since'].drop()
