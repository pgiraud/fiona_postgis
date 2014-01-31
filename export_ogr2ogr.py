#! /usr/bin/python

import subprocess

# The feature class to be created.
dst = "/tmp/output1.csv"

pg_connection = "PG:host=localhost user=www-data dbname=cisad password=www-data"
tablename = "ecoles_etude_sig_libre2"

subprocess.call(["ogr2ogr", "-f", "CSV", dst, pg_connection, tablename], )
