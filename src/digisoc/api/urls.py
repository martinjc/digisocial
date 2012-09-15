from django.conf.urls.defaults import patterns, include, url
from digisoc.api.views import *

urlpatterns = patterns('api.views',

    """
    Request crime data for area, given by north east and south west coordinates.

    GET parameters:

    ne - north east coordinate of bounding box
    sw - south west coordinate of bounding box

    returns: json list of crimes within bounding box:

    {
        crimes: [
            crime: {
                point: {
                    lat: X1,
                    lng: Y1
                }
                value: Z1
            },
            crime: {
                point: {
                    lat: X2,
                    lng: Y2
                }
                value: Z2
            },
            crime: {
                point: {
                    lat: X3,
                    lng: Y3
                }
                value: Z3
            }
        ]
    }


    usage:

    /crimes/?ne=X.XXXXXXX&sw=Y.YYYYYYY

    """
    url(r'crimes/', 'digisoc.api.crimes'),
)
