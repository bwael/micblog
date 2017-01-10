from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('role_id', Integer),
    Column('password_hash', String(length=128)),
    Column('location', String(length=64)),
    Column('about_me', String(length=140)),
    Column('member_since', DateTime, default=ColumnDefault(<function datetime.now at 0x04A11030>)),
    Column('last_seen', DateTime, default=ColumnDefault(<function datetime.now at 0x04A110C0>)),
    Column('avatar_hash', String(length=32)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['avatar_hash'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['avatar_hash'].drop()
