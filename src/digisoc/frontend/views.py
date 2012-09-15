# Create your views here.
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

ROOT_URL = getattr(settings, 'ROOT_URL', '')

@requires_csrf_token
def index(request):
    return render_to_response('index.html', {'root_url': ROOT_URL}, context_instance=RequestContext(request))
