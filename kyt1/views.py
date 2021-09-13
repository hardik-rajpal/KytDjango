from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
def land(request):
    return render(request,"land.html")
def timer(request):
    print(timezone.now())
    print(datetime.now())
    return render(request, "land.html", {'t1':timezone.now(), 't2':datetime.now()})