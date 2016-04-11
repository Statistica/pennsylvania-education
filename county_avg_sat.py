# Written by Jonathan Saewitz, released April 11th, 2016 for Statisti.ca
# Released under the MIT License (https://opensource.org/licenses/MIT)

from __future__ import division
import csv, requests, re, collections, plotly.plotly as plotly, plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout


schools=[]
with open('schools.csv', 'r') as f: #add all of the schools to the 'schools' list
	reader=csv.reader(f)
	next(reader) #skip header row
	for row in reader:
		try:
			schools.append({'aun': int(row[0]), 'county': row[5]}) #row[0] is the aun, row[5] is the county name
		except ValueError:
			pass


schools_sats=[]

with open('sat.csv', 'r') as f: #add each high school's sat score
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

district_avg_scores=[]
for county, scores in grouped.iteritems(): #get the average scores for each county
	district_avg_scores.append({'county': county, 'avg': sum(scores)/len(scores)})

#get each county's per capita income
for district_avg_score in district_avg_scores: #loop through every county's average sat scores
	with open('avg_income_pa.csv', 'r') as f:
		reader=csv.reader(f)
		for row in reader: #loop through every county average income
			if district_avg_score['county']==row[1]: #row[1] is the county name
				mean_income=int(row[2].replace("$", "").replace(",", "")) #format money (e.g. "$41,251"->41251)
				district_avg_score.update({'mean_income': mean_income})
				break #if we already found the county's income, no need to keep looping

sats=[]
incomes=[]
names=[]

for d in district_avg_scores:
	sats.append(d['avg'])
	incomes.append(d['mean_income'])
	names.append(d['county'])

trace=go.Scatter(
	x=incomes,
	y=sats,
	text=names,
	mode='markers'
)
data=[trace]
fig=go.Figure(data=data)
plotly.plot(fig) #plot the scatter plot!