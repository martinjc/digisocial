import sqlite3

def getCrimes(northest, eastest, southest, westest, startYear, startMonth, endYear, endMonth):
	con = sqlite3.connect("crime-data.db")
	c = con.cursor()
	crimes = c.execute("""SELECT * FROM crimes WHERE 
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
	
	crimeList = []
	for crime in crimes:
		crimeDict = {"crime":{
						"point":{
							"lat": crime[5],
							"lng": crime[6]
						},
						"date":{
							"year": crime[0],
							"month": crime[1]
						},
						"place_name": crime[7],
						"type": crime[8],
						"reported_by": crime[2]
					}}
		crimeList.append(crimeDict)
	return crimeList
	
def retrieveCrimes(ne, sw, sy, sm, ey, em):
	if sy == "":
		sy = 0
	if sm == "":
		sm = 0
	if ey == "":
		ey = 9999
	if em == "":
		em = 12
	startYear = int(sy)
	startMonth = int(sm)
	endYear = int(ey)
	endMonth = int(em)
	vertical1 = int((ne.split(",")[0]))
	vertical2 = int((sw.split(",")[0]))
	horizontal1 = int((ne.split(",")[1]))
	horizontal2 = int((sw.split(",")[1]))
	crimes = getCrimes(max(vertical1, vertical2), 
					max(horizontal1, horizontal2),
					min(vertical1, vertical2),
					min(horizontal1, horizontal2),
					startYear,
					startMonth,
					endYear,
					endMonth)
	return crimes