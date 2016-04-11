# Written by Jonathan Saewitz, released April 11th, 2016 for Statisti.ca
# Released under the MIT License (https://opensource.org/licenses/MIT)

from __future__ import division
import csv, requests, re, collections, plotly.plotly as plotly, plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout


schools=[]
with open('pa_schools.csv', 'r') as f: #add all of the schools to the 'schools' list
				       #pa_schools.csv from: http://www.edna.ed.state.pa.us/Screens/Extracts/wfExtractPublicSchools.aspx
	reader=csv.reader(f)
	next(reader) #skip header row
	for row in reader:
		try:
			schools.append({'aun': int(row[0]), 'county': row[5]}) #row[0] is the aun, row[5] is the county name
		except ValueError:
			pass


schools_sats=[]

with open('pa_sat_scores.csv', 'r') as f: #add each high school's sat score
					  #pa_sat_scores.csv from: http://www.education.pa.gov/K-12/Assessment%20and%20Accountability/Pages/SAT-and-ACT.aspx (Public School SAT Scores 2015)
	reader=csv.reader(f)
	for i in range(8): #skip header rows
		next(reader)
	for row in reader:
		try:
			schools_sats.append({'aun': int(row[0]), 'score': int(row[8])}) #add each school's AUN (Administrative Unit Number) and score
		except ValueError:
			pass
for school in schools_sats: #loop through every school's aun and score
	for s in schools: #loop through every school
		if s['aun']==school['aun']: #match the school's aun and the aun of the sat score list
			school.update({'county': s['county']}) #add the school's county
	del school['aun'] #remove the aun from the school

grouped=collections.defaultdict(list) #created a defaultdict

for county in schools_sats:
	grouped[county['county']].append(county['score']) #append the scores to counties in the defaultdict

county_avg_scores=[]
for county, scores in grouped.iteritems(): #get the average scores for each county
	county_avg_scores.append({'county': county, 'avg': sum(scores)/len(scores)})

#get each county's per capita income
for county_avg_score in county_avg_scores: #loop through every county's average sat scores
	with open('pa_avg_income.csv', 'r') as f: #pa_avg_income.csv from: https://en.wikipedia.org/wiki/List_of_Pennsylvania_counties_by_per_capita_income#Pennsylvania_counties_ranked_by_per_capita_income (from US Census Bureau)
		reader=csv.reader(f)
		for row in reader: #loop through every county average income
			if county_avg_score['county']==row[1]: #row[1] is the county name
				per_capita_income=int(row[2].replace("$", "").replace(",", "")) #format money (e.g. "$41,251"->41251)
				county_avg_score.update({'per_capita_income': per_capita_income})
				break #if we already found the county's income, no need to keep looping

sats=[]
incomes=[]
names=[]

f=open('counties_avg_sat.csv', 'w')
w=csv.writer(f)
w.writerow(["county", "average sat score", "per capita income"])
for c in county_avg_scores:
	sats.append(c['avg'])
	incomes.append(c['per_capita_income'])
	names.append(c['county'])
	w.writerow([c['county'], c['avg'], c['per_capita_income']])
f.close()

trace=go.Scatter(
	x=incomes,
	y=sats,
	text=names,
	mode='markers'
)
data=[trace]
fig=go.Figure(data=data)
# plotly.plot(fig) #plot the scatter plot!
