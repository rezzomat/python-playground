from sqlalchemy import engine_from_config
from sqlalchemy import create_engine
from sqlalchemy import DateTime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Query


DBSession = scoped_session(sessionmaker())
Base = declarative_base()


def initialize_sql(db_name, settings):
    """Called by the app on startup to setup bindings on the db

    :param db_name: db name, '/<relative path>' or '//<absolute path>', empty string for :memory:
    :param settings:
    :return:
    """
    # engine = engine_from_config(settings, 'sqlalchemy.')
    db_string = 'sqlite://' + db_name
    engine = create_engine(db_string, connect_args={'check_same_thread': False})

    if not DBSession.registry.has():
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)


def todict(self):
    """Method to turn an SA instance into a dict so we can output to json"""

    def convert_datetime(value):
        """We need to treat datetime's special to get them to json"""
        if value:
            return value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ""

    for col in self.__table__.columns:
        if isinstance(col.type, DateTime):
            value = convert_datetime(getattr(self, col.name))
        else:
            value = getattr(self, col.name)

        yield (col.name, value)


def iterfunc(self):
    """Returns an iterable that supports .next()
        so we can do dict(sa_instance)
    """
    return self.__todict__()


def fromdict(self, values):
    """Merge in items in the values dict into our object
       if it's one of our columns
    """
    for col in self.__table__.columns:
        if col.name in values:
            setattr(self, col.name, values[col.name])


Base.query = DBSession.query_property(Query)
Base.__todict__ = todict
Base.__iter__ = iterfunc
Base.fromdict = fromdict
