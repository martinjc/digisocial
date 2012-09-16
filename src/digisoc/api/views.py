# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest

import json
import crime_methods
import outcome_methods
import food_methods

def crimes(request):
    #
    # Prelim
    if request.method != 'GET':
        return HttpResponseBadRequest("GET calls only")

    params = request.GET

    req_params = ["ne", "sw"]
    for req_param in req_params:
        if req_param not in params:
            return HttpResponseBadRequest("missing param: %s" %(req_param))

    #
    # Grab params
    ne = params['ne']
    sw = params['sw']

    startYear = params.get('sy', None)
    startMonth = params.get('sm', None)
    endYear = params.get('ey', None)
    endMonth = params.get('em', None)

    try:
        crimeList = crime_methods.retrieveCrimes(ne, sw, startYear, startMonth, endYear, endMonth)
        crime_data = {'crimes': crimeList}
    	return return_data(request, crime_data)
    except Exception as e:
        return HttpResponseBadRequest( "Something went wrong. Blame Greenwood: %s" % e )

def outcomes(request):
    #
    # Prelim
    if request.method != 'GET':
        return HttpResponseBadRequest("GET calls only")

    params = request.GET

    req_params = ["ne", "sw"]
    for req_param in req_params:
        if req_param not in params:
            return HttpResponseBadRequest("missing param: %s" %(req_param))

    #
    # Grab params
    ne = params['ne']
    sw = params['sw']

    startYear = params.get('sy', None)
    startMonth = params.get('sm', None)
    endYear = params.get('ey', None)
    endMonth = params.get('em', None)

    try:
        outcomeList = outcome_methods.retrieveOutcomes(ne, sw, startYear, startMonth, endYear, endMonth)
        outcome_data = {'outcomes': outcomeList}
    	return return_data(request, outcome_data)
    except Exception as e:
        return HttpResponseBadRequest( "Something went wrong. Blame Greenwood: %s" % e )


def food_ratings(request):
    #
    # Prelim
    if request.method != 'GET':
        return HttpResponseBadRequest("GET calls only")

    params = request.GET

    req_params = ["ne", "sw"]
    for req_param in req_params:
        if req_param not in params:
            return HttpResponseBadRequest("missing param: %s" %(req_param))

    #
    # Grab params
    ne = params['ne']
    sw = params['sw']

    try:
        establishments_list = food_methods.retrieve_establishment_ratings(ne, sw)
        establishment_data = {'establishments': establishments_list}
    	return return_data(request, establishment_data)
    except Exception as e:
        return HttpResponseBadRequest( "Something went wrong. Blame Greenwood: %s" % e )

def return_data(request, data_dict):

    callback = request.GET.get('callback', None)

    if callback is None:
        return HttpResponse(json.dumps(data_dict), mimetype = 'application/json')
    else:
        return HttpResponse(callback + '(' + json.dumps(data_dict) + ')', mimetype = 'application/javascript')
