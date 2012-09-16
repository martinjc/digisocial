import sqlite3

def getOutcomes(northest, eastest, southest, westest, startYear, startMonth, endYear, endMonth):
	con = sqlite3.connect("outcome-data.db")
	c = con.cursor()
	outcomes = c.execute("""SELECT * FROM outcomes WHERE 
						year >= ? AND
						month >= ? AND
						year <= ? AND
						month <= ? AND
						latitude < ? AND
						longitude < ? AND
						latitude > ? AND
						longitude > ?""",
						(startYear, startMonth, endYear, endMonth, 
						northest, eastest, southest, westest)).fetchall()
	con.close()
	
	outcomeList = []
	for outcome in outcomes:
		outcomeDict = {"outcome":{
						"point":{
							"lat": outcome[5],
							"lng": outcome[6]
						},
						"date":{
							"year": outcome[0],
							"month": outcome[1]
						},
						"place_name": outcome[7],
						"outcome": outcome[8],
						"severity": outcome[9],
						"reported_by": outcome[2]
					}}
		outcomeList.append(outcomeDict)
	return outcomeList
	
def retrieveOutcomes(ne, sw, sy, sm, ey, em):
	if sy == None:
		sy = 0
	if sm == None:
		sm = 0
	if ey == None:
		ey = 9999
	if em == None:
		em = 12
	startYear = int(sy)
	startMonth = int(sm)
	endYear = int(ey)
	endMonth = int(em)
	vertical1 = float((ne.split(",")[0]))
	vertical2 = float((sw.split(",")[0]))
	horizontal1 = float((ne.split(",")[1]))
	horizontal2 = float((sw.split(",")[1]))
	outcomes = getOutcomes(max(vertical1, vertical2), 
					max(horizontal1, horizontal2),
					min(vertical1, vertical2),
					min(horizontal1, horizontal2),
					startYear,
					startMonth,
					endYear,
					endMonth)
	return outcomes