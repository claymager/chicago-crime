BEGIN;
  ALTER TABLE crimes ADD COLUMN loc_desc text;
  UPDATE crimes SET loc_desc = location_desc;

  UPDATE crimes SET loc_desc = 'CHA PARKING LOT/GROUNDS'
  WHERE loc_desc = 'CHA PARKING LOT'
     OR loc_desc = 'CHA PLAY LOT'
     OR loc_desc = 'CHA GROUNDS';

  UPDATE crimes SET loc_desc = 'CHA HALLWAY/STAIRWELL/ELEVATOR'
  WHERE loc_desc = 'CHA HALLWAY'
     OR loc_desc = 'CHA STAIRWELL'
     OR loc_desc = 'CHA ELEVATOR'
     OR loc_desc = 'CHA LOBBY'
     OR loc_desc = 'CHA BREEZEWAY';

  UPDATE crimes SET loc_desc = 'CHURCH/SYNAGOGUE/PLACE OF WORSHIP'
  WHERE loc_desc LIKE 'CHURCH%';

  UPDATE crimes SET loc_desc = 'BARBERSHOP'
  WHERE loc_desc LIKE 'BARBER%';

  UPDATE crimes SET loc_desc = 'PARKING LOT/GARAGE(NON.RESID.)'
  WHERE loc_desc = 'PARKING LOT';

  UPDATE crimes SET loc_desc = 'POOL ROOM'
  WHERE loc_desc = 'POOLROOM';

  UPDATE crimes SET loc_desc = 'TAXICAB'
  WHERE loc_desc = 'TAXI CAB';

  UPDATE crimes SET loc_desc = 'DRIVEWAY'
  WHERE loc_desc LIKE 'DRIVEWAY %';
  
  UPDATE crimes SET loc_desc = 'AIRPORT/AIRCRAFT'
  WHERE loc_desc LIKE 'AIR%';

  UPDATE crimes SET loc_desc = 'RESIDENCE'
  WHERE loc_desc LIKE 'RES%'
     OR loc_desc = 'HOUSE'
     OR loc_desc = 'PORCH'
     OR loc_desc LIKE 'DRIVEWAY%';

  UPDATE crimes SET loc_desc = 'NURSING HOME/RETIREMENT HOME'
  WHERE loc_desc = 'NURSING HOME';

  UPDATE crimes SET loc_desc = 'BAR/TAVERN/LIQUOR STORE'
  WHERE loc_desc = 'TAVERN'
     OR loc_desc = 'LIQUOR STORE'
     OR loc_desc = 'CLUB'
     OR loc_desc = 'BAR OR TAVERN';

  UPDATE crimes SET loc_desc = 'CTA PLATFORM'
  WHERE loc_desc LIKE 'CTA%PLATFORM';

  UPDATE crimes SET loc_desc = 'CTA TRAIN'
  WHERE loc_desc LIKE 'CTA%TRAIN';

  UPDATE crimes SET loc_desc = 'FACTORY'
  WHERE loc_desc LIKE 'FACTORY/%';

  UPDATE crimes SET loc_desc = 'HIGHWAY/EXPRESSWAY'
  WHERE loc_desc = 'HIGHWAY';

  UPDATE crimes SET loc_desc = 'JAIL'
  WHERE loc_desc LIKE 'JAIL %';

  UPDATE crimes SET loc_desc = 'LAKE/WATER/RIVER(BANK)'
   WHERE loc_desc LIKE 'LAKE%'
      OR loc_desc LIKE 'RIVER%'
      OR loc_desc LIKE 'BOAT%';
  
  UPDATE crimes SET loc_desc = 'BANK'
  WHERE loc_desc = 'CREDIT UNION';

  UPDATE crimes SET loc_desc = 'OTHER'
  WHERE loc_desc IN (
    SELECT loc_desc FROM crimes
    GROUP BY loc_desc
    HAVING count(*) < 100
  );
  
COMMIT;
