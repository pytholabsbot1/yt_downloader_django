from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pafy,os
from PIL import Image
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    

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
            res['cl_'] = "linkclass"

        except Exception as e:
            res['title'] = e
    #post(request)
    return render(request,'app1/index.html',context=res)


def artist(request):

    
    def ip():

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    
        return(ip)

    def get_file(ip_add):
        myfile = request.FILES['myfile'].open()
     
        img = Image.open(myfile)
        basewidth = 300

        if(img.size[0]>300):        
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)

        user_path = os.path.join(*['static','users',ip_add])

        if(not os.path.exists(user_path)):

            for f in ['','input','out']:
                os.mkdir(os.path.join(user_path,f))
             
        img.save(os.path.join(*[user_path,'input','img.jpg']))
        return(os.path.join(*[user_path,'input','img.jpg']))

###-----------------------------------------

    if request.method == 'POST' and request.FILES['myfile']:

        stored_img = os.path.join(BASE_DIR,get_file(ip()))
        script = os.path.join(*[BASE_DIR,'templates','art','evaluate.py'])
        chkpoint = os.path.join(*[BASE_DIR,'templates','art','rain_princess.ckpt'])
        out_dir = os.path.join(os.path.dirname(stored_img),'out')

        print(script,stored_img)
        os.system('python {} --checkpoint {} --in-path {} --out-path {}'.format(script,chkpoint,stored_img,out_dir))
        print('done')
        #os.system()
        # print(type(myfile),myfile)

    return render(request,'app1/art.html')



def post(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        HttpResponse(request)
