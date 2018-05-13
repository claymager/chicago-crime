CREATE OR REPLACE VIEW agg AS
  SELECT crimes.*, hood_ref.neighborhood,
         index_crime, violent_crime, property_crime, crime_against
  FROM crimes, hood_ref, fbi_codes
  WHERE crimes.latitude = hood_ref.latitude
    AND crimes.longitude = hood_ref.longitude
    AND crimes.fbi_code = fbi_codes.fbi_code;
