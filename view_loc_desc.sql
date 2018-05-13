SELECT loc_desc, count(distinct(fbi_code)), count(*)
FROM crimes
GROUP BY loc_desc;
