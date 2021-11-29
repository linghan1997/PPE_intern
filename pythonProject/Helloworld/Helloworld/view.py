from django.http import HttpResponse
from django.shortcuts import render
import os
from . import settings

def runoob(request):
    context = ["quzhu1", "quzhu2", "quzhu3"]
    return render(request, 'runoob.html', {"context": context})


# upload img and save it in the static/upfile folder
def upfile(request):
    return render(request, 'img_upload.html')

def savefile(request):
    if request.method=="POST":
        f = request.FILES['file']
        filepath = os.path.join(settings.MEDIA_ROOT, f.name)
        ## print(filepath)
        with open(filepath, 'wb') as fp:    # wb: open in bit form and only for write
            for info in f.chunks():    # write in segment to avoid occupying memory too much at one time
                fp.write(info)
                return HttpResponse('upload successful!')
    else:
        return HttpResponse('upload failed!')

def imgshow(request):
    return render(request, 'img_show.html')