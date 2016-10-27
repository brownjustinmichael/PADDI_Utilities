from os.path import expanduser

import numpy as np
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()


sqlalchemy_types = {np.float: sqlalchemy.Float,
                    np.int: sqlalchemy.Integer}


def Session(password = None, *args, **kwargs):
    """
    This function returns a :class:`sqlalchemy:Session` instance that is connected to the database on the system of choice. For the moment, this system is fixed to be on Loki and is password protected.

    :param args: Passed to :func:`sqlalchemy.orm.sessionmaker`
    :param kwargs: Passed to :func:`sqlalchemy.orm.sessionmaker`

    :rtype: :class:`sqlalchemy.orm.session.Session`
    :returns: The session instance that is connected either remotely or locally to the database
    """
    engine = sqlalchemy.create_engine('sqlite:///' + expanduser('~/paddi.db'), echo = False)
    Base.metadata.create_all(engine)

    return sqlalchemy.orm.sessionmaker(bind = engine)(*args, **kwargs)
