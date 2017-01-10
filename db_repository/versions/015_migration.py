from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
follow = Table('follow', post_meta,
    Column('follower_id', Integer, primary_key=True, nullable=False),
    Column('followed_id', Integer, primary_key=True, nullable=False),
    Column('timestamp', DateTime, default=ColumnDefault(<function datetime.now at 0x05814030>)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['follow'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['follow'].drop()
