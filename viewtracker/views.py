from django.http.request import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from .models import KYTVisitor, JCVisitor
import json
class VisitorData(APIView):
    def post(self, request:HttpRequest):
        data = json.loads(request.body.decode())["params"]["updates"][1]["value"].split(',')
        ip = data[0]
        loc = data[1] +','+ data[2]
        # try:
        site = data[4]
        if(site=="kyt"):
            vis,created = KYTVisitor.objects.get_or_create(userip=ip)
        else:
            vis, created = JCVisitor.objects.get_or_create(userip = ip)
        vis.freq+=1
        vis.loc = loc
        if(len(vis.dates)>1):
            print(vis.dates.split('f')[-2][-6:], data[3], 'f'.join(vis.dates.split('f')[:-1]))
            if(vis.dates.split('f')[-2][-6:]==data[3]):
                vis.dates = 'f'.join(vis.dates.split('f')[:-1]) + 'f'+str(vis.freq)
                print(vis.dates)
            else:
                vis.dates = vis.dates +'d'+ data[3] + 'f' +str(vis.freq )
        else:
            vis.dates = vis.dates +'d'+ data[3] + 'f' +str(vis.freq )
        vis.save()
        return Response("Success")