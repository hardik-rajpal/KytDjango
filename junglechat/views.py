from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status


from .serializers import QuoteSerializer

from .models import Quote, UserToken
from .serializers import ChatSnippetSerializer


from django.shortcuts import render, get_object_or_404
from .models import ChatSnippet
class snippets(APIView):
    def get(self, request):
        snips = ChatSnippet.objects.all()
        serializer = ChatSnippetSerializer(snips, many=True)
        return Response(serializer.data)
    def post(self,request):
        usrtkn = UserToken.objects.create()
        return Response(usrtkn.id)
    #TODO:implement put req. to maintain active status.
def jungleland(request):
    chats = ChatSnippet.objects.all()
    sep = '###'
    snips = sep.join([chat.snippet for chat in chats])
    return render(request,"jungle_land.html", {'snips':snips, 'sep':sep})
# Create your views here.
class quotes(APIView):
    def get(self, request,id=None,ip=None):
        snips = Quote.objects.all()
        serializer = QuoteSerializer(snips, many=True)
        return Response(serializer.data)
    def post(self,req,id=None,ip=None):
        # print(req,id,ip)
        if(id!=None and ip!=None):
            try:
                quote = Quote.objects.get(id=id)
                quote:Quote
                if(quote.likedBy!=''):
                    listips = quote.likedBy.split('*')
                    # print(listips)
                    if(not listips.__contains__(ip)):
                        listips.append(ip)
                        quote.likedBy = '*'.join(listips)
                    else:
                        listips.remove(ip)
                        quote.likedBy = '*'.join(listips)
                else:
                    quote.likedBy = ip
                    # print(quote.likedBy)
                quote.save()
                return Response(QuoteSerializer(quote).data)
            except:
                print('failed because quote DNE')
                pass
                return Response(QuoteSerializer(Quote.objects.all()[0]).data)
                