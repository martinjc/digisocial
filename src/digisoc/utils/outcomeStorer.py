import sqlite3
import csv
import os
import time
import coordConverter

# Reads CSV files and stores all data into an SQLITE database

def prepareTables(c):
	c.execute("""CREATE TABLE IF NOT EXISTS outcomes(
											year INT, 
											month INT, 
											reported_by VARCHAR, 
											easting INT, 
											northing INT,
											latitude REAL,
											longitude REAL,
											location VARCHAR,
											outcome_type VARCHAR,
											outcome_severity INT)""")

def getOutcomeSeverity(outcome):
	severities = {"Offender imprisoned":10,
				 "Offender given community penalty":6,
				 "Offender fined":8,
				 "Offender given conditional discharge":4,
				 "Offender otherwise dealt with":3,
				 "Suspect found not guilty":0,
				 "Offender given suspended prison sentence":9,
				 "Court case unable to proceed":4,
				 "Offender given absolute discharge":2,
				 "Offender required to pay compensation":6,
				 "Offender deprived of property":5,
				 "Suspect sent to Crown Court":8,
				 "No further action at this time":3,
				 "Suspect charged":4,
				 "Offender given a caution":2,
				 "Local resolution":2,
				 "Offender given penalty notice":4,
				 "Offender sentenced as part of another case":2}
	return severities[outcome]
	

def processFile(fileName, c):
	csvFile = open(rootDir+file, "r")
	reader = csv.reader(csvFile)
	count = 0
	for row in reader:
		if count > 0:
			if not row[0] == "":
				location = row[5].replace("On or near ", "")
				crimeDate = time.strptime(row[0], "%Y-%m")
				year = crimeDate[0]
				month = crimeDate[1]
				if not row[3] == "" or not row[4] == "":
					coords = coordConverter.convertCoords(int(row[3]), int(row[4]))
				else:
					coords = (-1, -1)
				latitude = coords[0]
				longitude = coords[1]
				severity = getOutcomeSeverity(row[6])
				c.execute("INSERT INTO outcomes VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
																		(year, 
																		month, 
																		row[1],
																		row[3],
																		row[4],
																		latitude,
																		longitude,
																		location,
																		row[6],
																		severity))
			if row[0] == "":
				csvFile.close()
				return
		count += 1
	
	csvFile.close()


rootDir = "/Users/willwebberley/Desktop/outcome_data/"

con = sqlite3.connect(rootDir+"outcome-data.db")
cursor = con.cursor()
prepareTables(cursor)
con.commit()
for subdir, dirs, files in os.walk(rootDir):
    for file in files:
    	if "csv" in file:
    		processFile(rootDir+file, cursor)
    		con.commit()
	    	
    		