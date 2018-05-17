#!/bin/bash
echo contact me for data
exit
dropdb chicago_crimes
createdb chicago_crimes
psql chicago_crimes < bin/build-database.sql

tar -xzvf data/crimes_2001_to_2017.tar.gz -C data/
for i in data/Chicago_Crimes_20*; do
  # remove headers
  sed -i '/Location/d' $i

  # corrupted records
  if [ $i = 'data/Chicago_Crimes_2001_to_2004.csv' ]; then
    sed -i '/18 08:55:02 AM/d' $i
  fi
  if [ $i = 'data/Chicago_Crimes_2008_to_2011.csv' ]; then
    sed -i '/9,-87.1:00:00 AM,/d' $i
  fi

  # remove duplicates
  sort -u $i -o $i
done

# build database
python queries.py
psql chicago_crimes < queries/fbi_codes.sql
psql chicago_crimes < queries/clean_locations.sql
psql chicago_crimes < queries/create_agg_view.sql
