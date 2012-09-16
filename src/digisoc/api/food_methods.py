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
	
if __name__ == '__main__':
    
    # from martin
    sw="51.50001163310808,-3.14414930343014"; ne="51.462594692253944,-3.2168478965697886"
    
    # cwmbran to the sea (lat,long)
    ne="51.650406754602294,-3.0157470703125"; sw="51.29541737712993,-3.464813232421875"
    
    # Cardiff's latitude vals should be around 51
    # Cardiff's longitude vals should be around -3.46

    #ne="-10000,-1000"; sw="10000,10000"
    #ne="1000,1000"; sw="1000,1000"
    print retrieve_establishment_ratings( ne, sw ) 
    print len( retrieve_establishment_ratings( ne, sw ) )
