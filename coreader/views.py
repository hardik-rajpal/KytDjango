from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from coreader.models import Book, Glossary, UserProfile
from coreader.serializers import BookSerializer, FullBookSerializer
# Create your views here.
class UserAuth(ViewSet):
    def login(self,request:HttpRequest):
        body = request.body.decode()
        return Response({})
    def register(self, request:HttpRequest):
        body = request.body.decode()
        return Response({})

class BookSet(ViewSet):
    def lowercaseHeaders(reqHandler):
        def lowercaser(*args,**kwargs):
            request:HttpRequest = args[1]
            headers = {}
            for key in request.headers.keys():
                headers[key.lower()] = request.headers[key]
            args[1].headers = headers
            return reqHandler(*args,**kwargs)
        return lowercaser
    def token_required(reqHandler):
        def tokenChecker(*args,**kwargs):
            request:HttpRequest = args[1]
            token = ''
            if(request.headers.keys().__contains__('coreaderkey')):
                token = request.headers['coreaderkey']
                if(token==settings.COREADER_KEY):
                    return reqHandler(*args,**kwargs)
                return Response({'message':'Wrong secret token in headers'},status=401)
            return Response({'message':'Secret Token missing in headers'},status=401)
        return tokenChecker
    @lowercaseHeaders
    @token_required
    def fetchBookSummaryByUser(self, request:HttpRequest):
        query = request.GET.dict()
        try:
            userid = int(query['userid'])
            isArchived = bool(query['archived'].lower()=='true')
        except:
            return Response({'message':'KeyError. Valid keys are userid and archived'},status=400)
        userpro = UserProfile.objects.get(id=userid)
        books = Book.objects.filter(user=userpro,archived=isArchived)
        data = BookSerializer(books,many=True).data
        return Response(data)
    @lowercaseHeaders
    @token_required
    def fetchFullBook(self, request:HttpRequest):
        query = request.GET.dict()
        qid = int(query['id'])
        print(qid)
        book = Book.objects.get(id=qid)
        return Response(FullBookSerializer(book).data)