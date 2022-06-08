from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
# Create your views here.
class UserAuth(ViewSet):
    def login(self,request:HttpRequest):
        body = request.body.decode()
        return Response({})
    def register(self, request:HttpRequest):
        body = request.body.decode()
        return Response({})