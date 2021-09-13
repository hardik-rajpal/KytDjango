import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
def land(request):
    return render(request,"land.html")
def timer(request, tzo):
    print(int(tzo))
    print(timezone.now())
    client_time = timezone.now() + datetime.timedelta(minutes = int(tzo) + 330)
    return render(request, "land.html", {'t1':timezone.now(), 't2':client_time})