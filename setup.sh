#!/bin/bash
dropdb chicago_crimes
createdb chicago_crimes
psql chicago_crimes < bin/build-database.sql

#tar -xzvf crimes_2001_to_2017.tar.gz -C data/
for i in data/Chicago_Crimes_20*; do
  sed -i '/Location/d' $i

  # corrupted records
  if [ $i = 'data/Chicago_Crimes_2001_to_2004.csv' ]; then
    sed -i '/18 08:55:02 AM/d' $i
  fi
  # TODO: verify on other files

  # remove duplicates
  sort -u $i -o $i
done

