from django.shortcuts import render
import json
import urllib.request

# Create your views here.
def index(request):
    if request.method == 'POST':
        city=request.POST['city']
    else:
        city='Enter a City'
    return render(request,'index.html',{'city':city})