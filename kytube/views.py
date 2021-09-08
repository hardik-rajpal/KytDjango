from django.shortcuts import render

# Create your views here.
def land(request):
    return render(request, "kytube_land.html")