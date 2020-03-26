from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
import requests
import time
import smtplib

from jinja2 import Template

from email.message import EmailMessage
from email.utils import make_msgid
#from background_task import background

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls() 
s.login("divyanshurai495@gmail.com", "slimming123")

f = open("send.html", "r")

def getData(url):
    return eval(requests.get('https://api.covid19india.org/data.json').text)

# Create your views here.
def home(request):
    dic={}
    dic['di'] = Sucriber.objects.all()
    if request.method == 'POST':
        form = SucriberForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'You Entered a Wrong Password')
            return redirect('home')
    else:
        form = SucriberForm()
        dic['form']=form

    html_doc = getData('https://api.covid19india.org/data.json')
    dic['active'] = html_doc['statewise'][0]['active']
    dic['confirmed'] = html_doc['statewise'][0]['confirmed']
    dic['deaths'] = html_doc['statewise'][0]['deaths']
    dic['recovered'] = html_doc['statewise'][0]['recovered']

    return render(request,'home.html',dic)
data_api = {'active': '0','confirmed': '0', 'deaths': '0','recovered': '0'}

def notify_user():
    data = getData('https://api.covid19india.org/data.json')
    bol = 0
    for i in ['active','confirmed', 'deaths','recovered']:
        if data['statewise'][0][i] != data_api[i]:
            bol=1
            break
    if bol:
        data_api['active'] = data['statewise'][0]['active']
        data_api['confirmed'] = data['statewise'][0]['confirmed']
        data_api['deaths'] = data['statewise'][0]['deaths']
        data_api['recovered'] = data['statewise'][0]['recovered']
        ppl = Sucriber.objects.all()
        tm = Template(f.read())
        msg_text1 = tm.render(confirmed=data_api['confirmed'],active=data_api['active'],recovered=data_api['recovered'],deaths=data_api['deaths'], data=data['statewise'])
        for i in ppl:
            msg = EmailMessage()
            msg['Subject'] = "Covid-19 Stats India"
            msg['From'] = "Divyanshu Rai <divyanshurai495@gmail.com>"
            msg['To'] = i.email
            asparagus_cid = make_msgid()
            msg.add_alternative(msg_text1,subtype='html')
            s.send_message(msg)
            print('send to: ',i.email)

#comment to add peopple
while True:
    notify_user()
    time.sleep(3600)