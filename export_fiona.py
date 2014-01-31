#! /bin/python

import logging
import sys

from sqlalchemy import *
from sqlalchemy.orm import *

engine = create_engine('postgresql://www-data:www-data@localhost/cisad', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


from sqlalchemy.ext.declarative import declarative_base
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

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

with fiona.open(
    '/tmp/test_fiona.tab',
    'w',
    driver='MapInfo File',
    schema={'geometry': 'Point', 'properties': [('numero', 'int')]}) as sink:
    for row in s:
        f = {}
        geom = loads(str(row.the_geom.geom_wkb))
        f['geometry'] = mapping(geom)
        f['properties'] = {}
        f['properties']['numero'] = row.numero
        sink.write(f)
        logging.info("Write done")
