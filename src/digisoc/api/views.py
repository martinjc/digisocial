# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest

import json

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
    ne_p = params['ne']
    sw_p = params['sw']
    try:
        ne = float(ne_p.strip())
        sw = float(sw_p.strip())
    except Exception:
        return HttpResponseBadRequest("failed to parse params: %s, %s" % (ne_p, sw_p))


    #
    # NEED TO DEAL WITH DATES AS WELL...
    #
    # Here's the magic, needs completing:
    #try:
    #    crime_data = ""
    #    return HttpResponse( crime_data )
    #except Exception:
    #    return HttpResponseBadRequest( "Something went wrong. Blame Greenwood." )

    crime_data = {'crimes': [{'crime': {'point': {'lat': 51.482, 'lng': -3.186}, 'value': 4}}, {'crime': {'point': {'lat': 51.382, 'lng': -3.176}, 'value': 2}}, {'crime': {'point': {'lat': 51.282, 'lng': -3.146}, 'value': 6}}]}
    return return_data(request, crime_data)

def return_data(request, data_dict):

    callback = request.GET.get('callback', None)

    if callback is None:
        return HttpResponse(json.dumps(data_dict), mimetype = 'application/json')
    else:
        return HttpResponse(callback + '(' + json.dumps(data_dict) + ')', mimetype = 'application/javascript')
