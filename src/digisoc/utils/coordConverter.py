import math

#####
# Convert Ordnance Survey grid reference easting/northing coordinate to (OSGB36) latitude/longitude
#
# DESCRIPTION
# params: easting(int), northing(int)
# returns: (latitude(float), longitude(float))(tuple) of grid reference
#
# EXAMPLE
# input: convert(263591, 196792)
# output: (51.614745 -3.964993)
#####

def toDeg(thingy):
	return thingy * 180 / math.pi;

def convert(easting, northing):
	E = easting
	N = northing
	
	a = 6377563.396 
	b = 6356256.910          # Airy 1830 major & minor semi-axes
	F0 = 0.9996012717                             # NatGrid scale factor on central meridian
	lat0 = 49*math.pi/180 
	lon0 = -2*math.pi/180  # NatGrid true origin
	N0 = -100000 
	E0 = 400000                     # northing & easting of true origin, metres
	e2 = 1 - (b*b)/(a*a)                     # eccentricity squared
	n = (a-b)/(a+b) 
	n2 = n*n 
	n3 = n*n*n
	
	lat=lat0 
	M=0
	
	while N-N0-M >= 0.00001:
		lat = (N-N0-M)/(a*F0) + lat
		
		Ma = (1 + n + (5/4)*n2 + (5/4)*n3) * (lat-lat0)
		Mb = (3*n + 3*n*n + (21/8)*n3) * math.sin(lat-lat0) * math.cos(lat+lat0)
		Mc = ((15/8)*n2 + (15/8)*n3) * math.sin(2*(lat-lat0)) * math.cos(2*(lat+lat0))
		Md = (35/24)*n3 * math.sin(3*(lat-lat0)) * math.cos(3*(lat+lat0))
		M = b * F0 * (Ma - Mb + Mc - Md)                # meridional arc
	
	cosLat = math.cos(lat) 
	sinLat = math.sin(lat)
	nu = a*F0/math.sqrt(1-e2*sinLat*sinLat)              # transverse radius of curvature
	rho = a*F0*(1-e2)/math.pow(1-e2*sinLat*sinLat, 1.5)  # meridional radius of curvature
	eta2 = nu/rho-1
	
	tanLat = math.tan(lat)
	tan2lat = tanLat*tanLat 
	tan4lat = tan2lat*tan2lat 
	tan6lat = tan4lat*tan2lat
	secLat = 1/cosLat
	nu3 = nu*nu*nu 
	nu5 = nu3*nu*nu 
	nu7 = nu5*nu*nu
	VII = tanLat/(2*rho*nu)
	VIII = tanLat/(24*rho*nu3)*(5+3*tan2lat+eta2-9*tan2lat*eta2)
	IX = tanLat/(720*rho*nu5)*(61+90*tan2lat+45*tan4lat)
	X = secLat/nu
	XI = secLat/(6*nu3)*(nu/rho+2*tan2lat)
	XII = secLat/(120*nu5)*(5+28*tan2lat+24*tan4lat)
	XIIA = secLat/(5040*nu7)*(61+662*tan2lat+1320*tan4lat+720*tan6lat)
	
	dE = (E-E0) 
	dE2 = dE*dE 
	dE3 = dE2*dE 
	dE4 = dE2*dE2 
	dE5 = dE3*dE2 
	dE6 = dE4*dE2 
	dE7 = dE5*dE2
	lat = lat - VII*dE2 + VIII*dE4 - IX*dE6
	lon = lon0 + X*dE - XI*dE3 + XII*dE5 - XIIA*dE7
	
	return ((toDeg(lat), toDeg(lon)))