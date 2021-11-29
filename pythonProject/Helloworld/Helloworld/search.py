from django.http import HttpResponse
from django.shortcuts import render

def search_form(request):
    return render(request, 'search_form.html')

def search(request):
    request.encoding='utf-8'
    if 'q' in request.GET and request.GET['q']:
        message = 'the content you are searching is: ' + request.GET['q']
    else:
        message = 'you have submited a blank form'
    return HttpResponse(message)