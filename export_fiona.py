#! /bin/python

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


s = session.query(Ecole).get(1)
print session.scalar(s.the_geom.wkt)

from shapely.geometry import shape
from fiona import collection

#with fiona.open('/tmp/test_fiona.shp', 'w') as sink:

#for f in s:
    #geom = shapely.wkb.loads(str(f.the_geom.geom_wkb))
