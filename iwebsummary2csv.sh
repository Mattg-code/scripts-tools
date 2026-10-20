#! /bin/bash
#
# cat figures.txt | iwebsummary2csv.hsh
# 

#tr  '\n' '\a' | sed 's/%/%\n/g' | tr -d ',' | tr -d '\a' | tr -d '£' | tr '\t' ',' | sed 's/ ,/,/g' | cut -f 1,4,6 -d ',' | sed 's/  (/,/' | tr -d ')' | sort -k 1

#tr  '\n' '\a' | sed 's/%/%\n/g' | tr -d ',' | tr -d '\a' | tr -d '£' | tr '\t' ',' | sed 's/ ,/,/g' | cut -f 1,2,3,4,6 -d ',' | sort -k 1

tr -cd '\11\12\15\40-\176' |\
tr  '\n' '\a' | sed 's/%/%\n/g' | tr -d ',' | tr -d '\a' | tr -d '£' | tr '\t' ',' |\
sed 's/ ,/,/g' | cut -f 1,2,3,4,6 -d ',' | sed 's/  (/,/' | tr -d ')' | sort -k 1
