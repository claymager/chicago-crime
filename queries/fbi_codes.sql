BEGIN;

SELECT fbi_code, count(*)
INTO fbi_codes
FROM crimes
GROUP BY fbi_code;

ALTER TABLE fbi_codes
  ADD COLUMN index_crime bool DEFAULT FALSE,
  ADD COLUMN violent_crime bool DEFAULT FALSE,
  ADD COLUMN property_crime bool DEFAULT FALSE,
  ADD COLUMN crime_against text;

UPDATE fbi_codes SET index_crime = TRUE
WHERE fbi_code = '01A'
   OR fbi_code = '02'
   OR fbi_code = '03'
   OR fbi_code = '04A'
   OR fbi_code = '04B'
   OR fbi_code = '05'
   OR fbi_code = '06'
   OR fbi_code = '07'
   OR fbi_code = '09';

UPDATE fbi_codes SET violent_crime = TRUE
WHERE fbi_code = '01A'
 OR fbi_code ='02'
 OR fbi_code ='03'
 OR fbi_code ='04A'
 OR fbi_code ='04B'
 OR fbi_code ='08A'
 OR fbi_code ='08B';

UPDATE fbi_codes SET property_crime = TRUE
WHERE fbi_code = '05' OR fbi_code = '06' OR fbi_code = '07' OR fbi_code = '09';

UPDATE fbi_codes SET crime_against = 'PERSONS'
WHERE fbi_code like '01%'
  OR fbi_code = '02'
  OR fbi_code like '04%'
  OR fbi_code like '08%'
  OR fbi_code = '17'
  OR fbi_code = '20'
 ;

UPDATE fbi_codes SET crime_against = 'PROPERTY'
WHERE property_crime = TRUE
  OR fbi_code = '03'
  OR fbi_code = '09'
  OR fbi_code = '10'
  OR fbi_code = '11'
  OR fbi_code = '12'
  OR fbi_code = '13'
  OR fbi_code = '14'
  ;

UPDATE fbi_codes SET crime_against = 'SOCIETY'
WHERE fbi_code = '15'
  OR fbi_code = '16'
  OR fbi_code = '18'
  OR fbi_code = '19'
  OR fbi_code = '21'
  OR fbi_code = '22'
  OR fbi_code = '24'
  OR fbi_code = '26'
  ;

SELECT * FROM fbi_codes ORDER BY fbi_code;

COMMIT;
