from django.shortcuts import render
from django.http import HttpResponse
import pafy
# Create your views here.


def index(request):
    res = {}
    if request.method == 'POST':
        url = request.POST.get('url')
        frmt = request.POST.get('service')
        try:
            video = pafy.new(url)
            res['title'] = video.title
            res['desc'] = video.description
            res['views'] = "views: "+str(video.viewcount)
            res['Download_text'] = "Download"
            res['url'] = video.getbestaudio().url if(frmt=='audio') else video.getbest().url


        except Exception as e:
            res['title'] = e
    #post(request)
    return render(request,'app1/index.html',context=res)

def post(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        HttpResponse(request)
