CREATE OR REPLACE VIEW agg AS
  SELECT crimes.*, 
         index_crime, violent_crime, property_crime, crime_against
  FROM crimes, fbi_codes
  WHERE crimes.fbi_code = fbi_codes.fbi_code;
