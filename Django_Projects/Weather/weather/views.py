from django.shortcuts import render
import json
import urllib.request

# Create your views here.
def index(request):
    if request.method == 'POST':
        city=request.POST['city']
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=7bb90ceb6c547e3c7aed7c71a5b743f1'
        res = urllib.request.urlopen(url).read()
        json_data=json.loads(res)    
        data={
            'country_code':str(json_data['sys']['country']),
            'coordinate':str(json_data['coord']['lon'])+' '+str(json_data['coord']['lat']),
            'temp': f"{json_data['main']['temp'] - 273:.2f}°C",
            'pressure':f"{str(json_data['main']['pressure'])} hPa",
            'humidity':f"{str(json_data['main']['humidity'])}%"
        }
        print(json_data)
    else:
        city='Enter a City'
        data={}
    return render(request,'index.html',{'data':data,'city':city})
