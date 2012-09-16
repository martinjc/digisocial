import sqlite3

def getNumCrimes(northest, eastest, southest, westest, startYear, startMonth, endYear, endMonth):
	con = sqlite3.connect("crime-data.db")
	c = con.cursor()
	crimes = c.execute("""SELECT year FROM crimes WHERE 
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
	return len(crimes)

def getNumOutcomeType(type, northest, eastest, southest, westest, startYear, startMonth, endYear, endMonth):
	con = sqlite3.connect("outcome-data.db")
	c = con.cursor()
	outcomes = c.execute("""SELECT outcome_type FROM outcomes WHERE
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
	counter = 0
	for outcome in outcomes:
		if type in outcome[0]:
			counter += 1
	return counter

def getProportionImprisoned(ne, sw, sy, sm, ey, em):
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
	numCrimes = getNumCrimes(max(vertical1, vertical2), 
					max(horizontal1, horizontal2),
					min(vertical1, vertical2),
					min(horizontal1, horizontal2),
					startYear,
					startMonth,
					endYear,
					endMonth)
	numImprisoned = getNumOutcomeType("prison", max(vertical1, vertical2), 
					max(horizontal1, horizontal2),
					min(vertical1, vertical2),
					min(horizontal1, horizontal2),
					startYear,
					startMonth,
					endYear,
					endMonth)
	return str(round (((numImprisoned + 0.0) / (numCrimes + 0.0) * 100), 2))+"%"