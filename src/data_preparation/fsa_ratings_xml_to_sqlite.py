"""Translate an XML file of food hygene ratings for a given local authority
to an SQL database. Values in the XML tree below a particular establishment 
node are flattened into a database row.

URLs for the dataset:
    http://data.gov.uk/dataset/uk-food-hygiene-rating-data
    http://ratings.food.gov.uk/open-data/en-GB
"""

from xml.dom.minidom import parse, parseString
import csv 
import sqlalchemy as alch
import sqlalchemy.orm        
import sqlalchemy.exc
import copy
        
def xml_to_dict( node, out_dict=None ):
    """Generate a flat dictionary from all leaf descendants of `node`. Assumes
    that no two leaf nodes have the same tag name."""
    
    if out_dict is None:
        # First call -- begin recusrion 
        out_dict = {}
        for child in node.childNodes:
            for grandchild in child.childNodes:
                xml_to_dict( grandchild, out_dict=out_dict )
    elif not node.hasChildNodes():
        # Recusrion base case
        tag = node.parentNode.localName 
        val = node.nodeValue
        out_dict[tag] = val
    else:
        # Recursive step
        for child in node.childNodes:
            xml_to_dict( child, out_dict=out_dict )
    return out_dict

if __name__ == '__main__':
    
    #
    # Params
    in_fpath = './cardiff.xml'
    out_fpath = 'fsa_food_ratings.db'

    #
    # Input prep
    dom = parse( in_fpath )

    collection = dom.getElementsByTagName( 'EstablishmentCollection' )[0]
    establishment_nodes = collection.getElementsByTagName( 'EstablishmentDetail' )

    print "num establishment nodes", len( establishment_nodes )
    
    #
    # Load establishments into dicts
    establishments = []
    
    for establishment in establishment_nodes:
        d = xml_to_dict( establishment )
        if ( 'Latitude' not in d ) or ( 'Longitude' not in d ):
            continue
        
        # swap around the lonitude and latitude values 
        # because the FSA got them wrong!!!
        actual_lat = d['Longitude']
        actual_long = d['Latitude']
        d['Latitude'] = actual_lat
        d['Longitude'] = actual_long
        
        establishments.append( d )
    
    num_estabs = len(establishments)
    
    #
    # DB
    #   http://docs.sqlalchemy.org/en/rel_0_5/ormtutorial.html
    engine = alch.create_engine( 'sqlite:///%s' % out_fpath )
    
    #
    # Metadata (schema etc)
    metadata = alch.MetaData( engine )
    
    fieldnames = establishments[0].keys()
    print fieldnames
    tab_cols = []
    for fieldname in fieldnames: 
        if fieldname in ('LocalAuthorityBusinessID', 'LocalAuthorityCode'):
            col = alch.Column(fieldname, alch.String(), primary_key=True )
        else:
            if fieldname in [ 'Longitude', 'Latitude' ]:
                col = alch.Column(fieldname, alch.Float() )
            else:
                col = alch.Column(fieldname, alch.String() )
        
        tab_cols.append( col )
    
    estab_table = alch.Table( 'establishments', metadata, *tab_cols )
    
    metadata.create_all( engine )
    estab_table.delete()
    
    #
    # Insert data
    class Establishment( object ):
        def __init__( self, **kwargs ):
            for key, val in kwargs.iteritems():
                setattr( self, key, val )
    
    sqlalchemy.orm.mapper( Establishment, estab_table )
    session = sqlalchemy.orm.sessionmaker( engine )()
    
    num_collisions = 0
    
    for estab_d in establishments:
        obj = Establishment( **estab_d )
        
        db_obj = session.query(Establishment).get((obj.LocalAuthorityBusinessID,obj.LocalAuthorityCode))
        if db_obj is None:
            session.add( obj )
        else:
            num_collisions += 1
    
	session.commit()
    
    print "SUCCESS"
    print "num_estabs", num_estabs
    print "num collisions:", num_collisions
    
    
    
    
    