#! /bin/python

import logging
import sys

from sqlalchemy import *
from sqlalchemy.orm import *

engine = create_engine('postgresql://www-data:www-data@localhost/cisad', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.util import class_mapper
from datetime import datetime
from geoalchemy import *

metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)

# Define the model classes
class Ecole(Base):
    __tablename__ = 'ecoles_etude_sig_libre2'
    __table_args__ = {'autoload': True}
    the_geom = GeometryColumn(Point(2))

GeometryDDL(Ecole.__table__)

#s = session.query(Ecole).get(1)
#print s.the_geom.wkt

s = session.query(Ecole).filter(Ecole.the_geom!=None).limit(10).all()
#print session.scalar(s.the_geom.wkt)

from shapely.wkb import loads
from shapely.geometry import mapping
import fiona
from fiona import collection

import sqlalchemy

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def _col_type_mapping(cls):
    if isinstance(cls, sqlalchemy.types.CHAR) or \
       isinstance(cls, sqlalchemy.types.VARCHAR):
        # TODO manage string length
        return 'str'
    elif isinstance(cls, sqlalchemy.types.INTEGER):
        return 'int'
    elif isinstance(cls, sqlalchemy.types.FLOAT) or \
         isinstance(cls, sqlalchemy.dialects.postgresql.base.DOUBLE_PRECISION):
        return 'float'
    else:
        print type(cls)
        return 'str'



# create the schema
schema = {'properties': []}
properties = schema['properties']
for p in class_mapper(Ecole).iterate_properties:
    if isinstance(p, ColumnProperty):
        if len(p.columns) != 1:  # pragma: no cover
            raise NotImplementedError
        col = p.columns[0]
        if isinstance(col.type, Geometry):
            schema['geometry'] = 'Point'
            print col
        elif not col.foreign_keys:
            # TODO use col.type
            properties.append((p.key, _col_type_mapping(col.type)))

with fiona.open(
    '/tmp/test_fiona.tab',
    'w',
    driver='MapInfo File',
    schema=schema) as sink:
    for row in s:
        f = {}
        geom = loads(str(row.the_geom.geom_wkb))
        f['geometry'] = mapping(geom)
        f['properties'] = {}
        for p in properties:
            f['properties'][p[0]] = getattr(row, p[0])
        sink.write(f)
        logging.info("Write done")
