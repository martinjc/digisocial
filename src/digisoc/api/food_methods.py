import sqlite3

def get_establishment_ratings(northest, eastest, southest, westest):
	con = sqlite3.connect("fsa_food_ratings.db")
	con.row_factory = sqlite3.Row

	establishments = con.execute("""SELECT * FROM establishments WHERE
						Latitude < ? AND
						Longitude < ? AND
						Latitude > ? AND
						Longitude > ?""",
						(northest, eastest, southest, westest)).fetchall()
	con.close()
	establishments = [ dict(est) for est in establishments ]
	return establishments

def retrieve_establishment_ratings(ne, sw):
	vertical1 = float((ne.split(",")[0]))
	vertical2 = float((sw.split(",")[0]))
	horizontal1 = float((ne.split(",")[1]))
	horizontal2 = float((sw.split(",")[1]))

	estabs = get_establishment_ratings(max(vertical1, vertical2),
					max(horizontal1, horizontal2),
					min(vertical1, vertical2),
					min(horizontal1, horizontal2),)
	return estabs
