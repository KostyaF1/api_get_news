from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError
)

from django.shortcuts import get_object_or_404, render, render_to_response


def main_page(request):
	return render(request, 'index.html')


def handler400(request, exception, template_name='400.html'):
    response = render_to_response('400.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 400
    return response    


def handler403(request, exception, template_name='403.html'):
    response = render_to_response('403.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 403
    return response    


def handler404(request, exception, template_name='404.html'):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response    


def handler500(request, template_name='500.html'):
    return HttpResponseServerError()
