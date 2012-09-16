from django.conf.urls.defaults import patterns, include, url
from digisoc.api.views import *

urlpatterns = patterns('',


    # Request crime data for area, given by north east and south west coordinates.
    #
    # GET parameters:
    #
    # ne - north east coordinate of bounding box
    # sw - south west coordinate of bounding box
    # from - start date (optional)
    # to - end date (optional)
    #
    # returns: json list of crimes within bounding box:
    #
    # {
    #     crimes: [
    #         crime: {
    #             point: {
    #                 lat: X1,
    #                 lng: Y1
    #             }
    #            value: Z1
    #         },
    #         crime: {
    #             point: {
    #                 lat: X2,
    #                 lng: Y2
    #             }
    #             value: Z2
    #         },
    #         crime: {
    #             point: {
    #                 lat: X3,
    #                 lng: Y3
    #             }
    #             value: Z3
    #         }
    #     ]
    # }
    #
    #
    # usage:
    #

    (r'crimes/$', crimes),
    (r'crimeIntensity/$', crimeIntensityInArea),
    (r'crimeInArea/$', crimesInArea),
    (r'outcomes/$', outcomes),
    (r'food/$', food_ratings),
)
