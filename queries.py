import psycopg2 as pg
import pandas.io.sql as pd_sql


connection_args = {
    'host': '127.0.0.1', 
    'user': 'john',
    'password': 'arst',
    'dbname': 'chicago_crimes',
    'port': 5432}

def get_data_from_sql(target, features_sql, since="2015-01-01"):
    """
    Queries my local server
    takes two strings
    returns two dataframes
    """
    connection = pg.connect(**connection_args)
    query = "SELECT {} FROM agg WHERE latitude > 36.62 AND datetime > '{}'"
    ys = pd_sql.read_sql(query.format(target, since), connection)
    Xs = pd_sql.read_sql(query.format(features_sql, since), connection)
    connection.close()
    return Xs, ys

def get_loc_desc():
    connection = pg.connect(**connection_args)
    query = "SELECT distinct(loc_desc) FROM agg"
    return pd_sql.read_sql(query, connection)

build_tables_sql = """
CREATE TABLE crimes(
	id	 	integer,
	case_number	varchar(9),
	datetime timestamp,
	block 		text,	
	primary_type 	text,
	description 	text,
	location_desc 	text,
	domestic 	boolean,
	fbi_code 	char(3),
	latitude 	float,
	longitude 	float
);

CREATE TEMP TABLE crimes_csv(
	unknown		integer,
	id	 	integer,
	case_number	varchar(9),
	datestr 	char(22),
	block 		text,	
	iucr 		char(4),
	primary_type 	text,
	description 	text,
	location_desc 	text,
	arrest 		boolean,
	domestic 	boolean,
	beat 		integer,
	district 	float,
	ward 		float,
	community_area	float,
	fbi_code 	char(3),
	x_coord		float,
	y_coord		float,
	year 		char(4),
	updated_on	char(22),
	latitude 	float,
	longitude 	float,
	location	varchar(29)
);
"""

load_csv_str = """
TRUNCATE TABLE crimes_csv;

copy crimes_csv FROM '{}' DELIMITER ',' CSV; 

INSERT INTO crimes 
( id,
  case_number,
  datetime,
  block,
  primary_type,
  description,
  location_desc,
  domestic,
  fbi_code,
  latitude,
  longitude )
SELECT
 id,
  case_number,
  CAST (datestr AS TIMESTAMP),
  block,
  primary_type,
  description,
  location_desc,
  domestic,
  fbi_code,
  latitude,
  longitude 
FROM crimes_csv
WHERE
  longitude IS NOT NULL
;"""
