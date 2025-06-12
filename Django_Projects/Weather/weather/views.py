from django.shortcuts import render
import json
import urllib.request

# Create your views here.
def index(request):
    if request.method == 'POST':
        city=request.POST['city']
        res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q'+city+"&appid=7bb90ceb6c547e3c7aed7c71a5b743f1").read()
    else:
        city='Enter a City'
    return render(request,'index.html',{'city':city})