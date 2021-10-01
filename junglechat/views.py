from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from .serializers import ChatSnippetSerializer


from django.shortcuts import render, get_object_or_404
from .models import ChatSnippet
class snippets(APIView):
    def get(self, request):
        snips = ChatSnippet.objects.all()
        serializer = ChatSnippetSerializer(snips, many=True)
        print(serializer.data)
        return Response(serializer.data)
    def post(self):
        pass
def jungleland(request):
    chats = ChatSnippet.objects.all()
    sep = '###'
    snips = sep.join([chat.snippet for chat in chats])
    return render(request,"jungle_land.html", {'snips':snips, 'sep':sep})
# Create your views here.
