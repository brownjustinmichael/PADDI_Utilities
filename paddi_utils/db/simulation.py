import enum
from os.path import abspath

import sqlalchemy
from sqlalchemy.orm import relationship, aliased

from paddi_utils.data import Parameters
from paddi_utils.db.session import Base, sqlalchemy_types


class Simulation(Base):
    __tablename__ = "simulations"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    path = sqlalchemy.Column(sqlalchemy.String)
    tags = relationship("Tag", backref="simulation")
    output_files = relationship("OutputFile", backref="simulation")

    class Query(object):
        def __init__(self, query, name):
            super(Simulation.Query).__init__()
            self.query = query
            self.name = name

        def __lt__(self, other):
            alias = aliased(Tag)
            return self.query.filter(alias.name == self.name, alias.value < other).join(alias)

        def __le__(self, other):
            alias = aliased(Tag)
            return self.query.filter(alias.name == self.name, alias.value <= other).join(alias)

        def __gt__(self, other):
            alias = aliased(Tag)
            return self.query.filter(alias.name == self.name, alias.value > other).join(alias)

        def __ge__(self, other):
            alias = aliased(Tag)
            return self.query.filter(alias.name == self.name, alias.value >= other).join(alias)

        def __eq__(self, other):
            alias = aliased(Tag)
            return self.query.filter(alias.name == self.name, alias.value == other).join(alias)

        def __ne__(self, other):
            alias = aliased(Tag)
            return self.query.filter(alias.name == self.name, alias.value != other).join(alias)

    @classmethod
    def from_params(cls, params, path="."):
        self = cls(path=abspath(path))
        for name, type in Parameters.default_format:
            setattr(self, name, params[name])
        return self


class Tag(Base):
    __tablename__ = "tags"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    value = sqlalchemy.Column(sqlalchemy.Float)
    sim_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('simulations.id'))


class OutputFile(Base):
    __tablename__ = "outputfiles"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    file = sqlalchemy.Column(sqlalchemy.String)
    sim_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('simulations.id'))

    filenames = {"diagnostic": "OUT",
                 "dump": "DUMP",
                 "jdata": "j__data",
                 "xyspec": "XY_SPEC",
                 "zprof": "ZPROF",
                 "zspec": "Z_SPEC"}

    filetypes = [name for name in filenames]

    type = sqlalchemy.Column(sqlalchemy.Enum(*filetypes))



for name, type in Parameters.default_format:
    setattr(Simulation, name, sqlalchemy.Column(sqlalchemy_types[type]))
