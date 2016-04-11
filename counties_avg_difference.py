# Written by Jonathan Saewitz, released April 11th, 2016 for Statisti.ca
# Released under the MIT License (https://opensource.org/licenses/MIT)

import csv, operator

counties=[]

with open('counties_avg_sat.csv', 'r') as f: #load all of the counties
	reader=csv.reader(f)
	reader.next() #skip header row
	for row in reader:
		counties.append({'county': row[0], 'avg_sat': float(row[1]), 'per_capita_income': int(row[2])})

for county in counties:
	expected_sat=0.007214185143521261*county['per_capita_income'] + 1278.0473160791375 #calculate the expected sat
	difference=county['avg_sat']-expected_sat
	county.update({'expected_sat': expected_sat, 'difference': difference}) #update the county
	del county['per_capita_income'] #delete the per_capita_income from the county, we don't need it anymore

f=open('counties_avg_sat_difference.csv', 'w') #save the counties to a .csv
w=csv.writer(f)
w.writerow(["county", "average sat score", "expected sat score", "difference from expected"])
for c in sorted(counties, key=operator.itemgetter('difference'), reverse=True):
	w.writerow([c['county'], c['avg_sat'], round(c['expected_sat'], 2), round(c['difference'], 2)])
f.close()
