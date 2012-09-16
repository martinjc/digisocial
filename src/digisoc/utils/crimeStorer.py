import sqlite3
import csv
import os
import time
import coordConverter

# Reads CSV files and stores all data into an SQLITE database

def prepareTables(c):
	c.execute("""CREATE TABLE IF NOT EXISTS crimes(
											year INT, 
											month INT, 
											reported_by VARCHAR, 
											easting INT, 
											northing INT,
											latitude REAL,
											longitude REAL,
											location VARCHAR,
											crime_type VARCHAR,
											crime_severity INT)""")
	

def getCrimeSeverity(crime):
	severities = {"Burglary":6,
				  "Anti-social behaviour":4,
				  "Robbery":7,
				  "Vehicle crime":8,
				  "Violent crime":10,
				  "Other crime":5,
				  "Public disorder and weapons":10,
				  "Shoplifting":6,
				  "Criminal damage and arson":9,
				  "Other theft":6,
				  "Drugs":6}
	return severities[crime]

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
				severity = getCrimeSeverity(row[6])
				c.execute("INSERT INTO crimes VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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


rootDir = "/Users/willwebberley/Desktop/crime_data/"

con = sqlite3.connect(rootDir+"crime-data.db")
cursor = con.cursor()
prepareTables(cursor)
con.commit()
for subdir, dirs, files in os.walk(rootDir):
    for file in files:
    	if "csv" in file:
    		processFile(rootDir+file, cursor)
    		con.commit()
	    	
    		