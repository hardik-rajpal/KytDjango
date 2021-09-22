from django.shortcuts import render
from .models import ChatSnippet
def jungleland(request):
    chats = ChatSnippet.objects.all()
    sep = '###'
    snips = sep.join([chat.snippet for chat in chats])
    return render(request,"jungle_land.html", {'snips':snips, 'sep':sep})
# Create your views here.
