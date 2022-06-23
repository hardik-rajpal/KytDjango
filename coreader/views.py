import json
from typing import List
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from coreader.models import Book, Glossary, Note, UserProfile, WordBlock,models
from coreader.serializers import BookSerializer, FullBookSerializer, GlossarySerializer, NoteSerializer, UserProfileSerializer
# Create your views here.
class UserAuth(ViewSet):
    def login(self,request:HttpRequest):
        body = request.body.decode()
        return Response({})
    def register(self, request:HttpRequest):
        body = request.body.decode()
        return Response({})
class WordBlockToPush:
    id:int
    word:str
    isKnown:bool
    comment:str
    def fromDict(body):
        word = WordBlockToPush()
        word.id = body["id"]
        word.word = body["word"]
        word.isKnown = body["isKnown"]
        word.comment = body["comment"]
        return word
class GlossaryToPush:
    id:int
    title:str
    ownerType:str
    ownerID:int
    words:List[WordBlockToPush]

    def fromDict(body):
        glossary = GlossaryToPush()
        glossary.id = body["id"]
        glossary.title = body["title"]
        glossary.ownerType = body["ownerType"]
        glossary.ownerID = body["ownerID"]
        glossary.words = list(map(lambda x:WordBlockToPush.fromDict(x),body["words"]))
        return glossary
class NoteToPush:
    id:int
    title:str
    content:str
    book:int
    def fromDict(body):
        note = NoteToPush()
        note.id = body["id"]
        note.title = body["title"]
        note.content = body["content"]
        note.book = body["book"]
        return note
class BookToPush:
    id:int
    user:int
    title:str
    coverLink:str
    numPages:int
    bookmark:int
    uiColor:int
    pdfPath:int
    archived:bool
    def fromBody(body):
        book = BookToPush()
        book.id = body["id"]
        book.user = body["user"]
        book.title = body["title"]
        book.coverLink = body["coverLink"]
        book.numPages = body["numPages"]
        book.bookmark = body["bookmark"]
        book.uiColor = body["uiColor"]
        book.pdfPath = body["pdfPath"]
        book.archived = body["archived"]
        return book
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
    @lowercaseHeaders
    def tokenChecker(*args,**kwargs):
        request:HttpRequest = args[1]
        token = ''
        if(request.headers.keys().__contains__('coreaderkey')):
            token = request.headers['coreaderkey']
            if(token==settings.COREADER_KEY):
                return reqHandler(*args,**kwargs)
            return Response({'message':'Wrong secret token in headers'},status=401)
        return Response({'message':'Secret Token missing in headers'},status=403)
    return tokenChecker
def usertoken_required(reqHandler):
    @lowercaseHeaders
    @token_required
    def userTokenChecker(*args,**kwargs):
        request:HttpRequest = args[1]
        if(request.headers.keys().__contains__('usertoken')):
            args[1].user = UserProfile.objects.get(token=request.headers['usertoken'])
            return reqHandler(*args,**kwargs)
        return Response({'message':'User Token missing in headers'},status=401)
    return userTokenChecker
class BookSet(ViewSet):
    modelDict = {
        'book':Book,
        'glossary':Glossary,
        'note':Note,
        'wordblock':WordBlock
    }
    @usertoken_required
    def fetchBookSummaryByUser(self, request:HttpRequest):
        query = request.GET.dict()
        try:
            isArchived = bool(query['archived'].lower()=='true')
        except:
            return Response({'message':'KeyError. archived key not provided'},status=400)
        userpro = request.user
        books = Book.objects.filter(user=userpro,archived=isArchived)
        data = BookSerializer(books,many=True).data
        return Response(data)
    @usertoken_required
    def fetchFullBook(self, request:HttpRequest):
        query = request.GET.dict()
        qid = int(query['id'])
        book:Book = Book.objects.get(id=qid)
        if(book.user.id==request.user.id):
            return Response(FullBookSerializer(book).data)
        return Response('Not your book, homie',status=403)
    @usertoken_required
    def pushBooks(self, request:HttpRequest):
        body = json.loads(request.body.decode())
        body:List[BookToPush]
        serializedBooks = []
        for book in body:
            book = BookToPush.fromBody(book)
            if(book.id==-1):
                user:UserProfile = UserProfile.objects.get(id=book.user)
                if(user.id!=request.user.id):
                    continue
                bookobj:Book = Book.objects.create(
                    user=user,
                    title=book.title,
                    coverLink=book.coverLink,
                    numPages=book.numPages,
                    bookmark=book.bookmark,
                    uiColor=book.uiColor,
                    pdfPath=book.pdfPath,
                    archived=book.archived
                    )
            else:
                bookobj = Book.objects.get(id=book.id)
                if(bookobj.user.id!=request.user.id):
                    continue
                bookobj.title = book.title
                bookobj.coverLink=book.coverLink
                bookobj.numPages=book.numPages
                bookobj.bookmark=book.bookmark
                bookobj.uiColor=book.uiColor
                bookobj.pdfPath=book.pdfPath
                bookobj.archived=book.archived
                bookobj.save()
            serializedBooks.append(BookSerializer(bookobj).data)
        return Response(serializedBooks)
    @usertoken_required
    def pushGlossaries(self,request:HttpRequest):
        body = json.loads(request.body.decode())
        serializedGlossaries = []
        for glossary in body:
            glossary = GlossaryToPush.fromDict(glossary)
            if(glossary.ownerType=='book'):
                book:Book = Book.objects.get(id=glossary.ownerID)
                if(book.user.id!=request.user.id):
                    serializedGlossaries.append(f'not your book {glossary.ownerID}')
                    continue
            else:
                userpro = UserProfile.objects.get(id=glossary.ownerID)
                if(userpro.id!=request.user.id):
                    serializedGlossaries.append(f'not your profile {glossary.ownerID}')
            if(glossary.id==-1):
                glossaryobj = Glossary.objects.create(
                    title = glossary.title,
                    ownerType = 'book',
                    ownerID = glossary.ownerID
                )
            else:
                glossaryobj:Glossary = Glossary.objects.get(id=glossary.id)
                glossaryobj.title = glossary.title
                glossaryobj.ownerID = glossary.ownerID
                glossaryobj.save()
            for wb in glossary.words:
                if(wb.id==-1):
                    wordobj:WordBlock = WordBlock.objects.create(
                        word=wb.word,
                        isKnown=wb.isKnown,
                        comment=wb.comment,
                        glossary=glossaryobj
                    )
                else:
                    wordobj:WordBlock = WordBlock.objects.get(id=wb.id)
                    wordobj.word=wb.word
                    wordobj.isKnown=wb.isKnown
                    wordobj.comment=wb.comment
                    wordobj.save()
            serializedGlossaries.append(GlossarySerializer(glossaryobj).data)
        return Response(serializedGlossaries)
    @usertoken_required
    def pushNotes(self,request:HttpRequest):
        body = json.loads(request.body.decode())
        serializedNotes=[]
        for note in body:
            note = NoteToPush.fromDict(note)
            bookobj:Book = Book.objects.get(id=note.book)
            if(bookobj.user.id!=request.user.id):
                serializedNotes.append(f'not your book {note.book}')
                continue
            if(note.id==-1):
                noteobj = Note.objects.create(
                    title=note.title,
                    content=note.content,
                    book=bookobj
                )
            else:
                noteobj:Note = Note.objects.get(id=-1)
                noteobj.title=note.title
                noteobj.content=note.content
                noteobj.book = bookobj
                noteobj.save()
            serializedNotes.append(NoteSerializer(noteobj).data)
        return Response(serializedNotes)
    @usertoken_required
    def pushDeletes(self, request:HttpRequest):
        body = json.loads(request.body.decode())
        deleted = []
        for i,item in enumerate(body):
            model:models.Model = self.modelDict[item['model']]
            try:
                model.objects.get(id=item['id']).delete()
                if(item['model']=='book'):
                    Glossary.objects.all().filter(ownerType='book',ownerID=item['id']).delete()
                deleted.append(i)
            except:
                continue
        return Response(deleted)
class UserSet(ViewSet):
    @usertoken_required
    def getUserDetails(self,request:HttpRequest):
        return Response(UserProfileSerializer(request.user).data)
    @token_required
    def loginUser(self,request:HttpRequest):
        body = json.loads(request.body.decode())
        identifier = body['identifier']
        try:
            user:UserProfile = UserProfile.objects.get(identifier=identifier)
        except:
            favs:Glossary = Glossary.objects.create(
                title='Favourites',
                ownerType='user',
                ownerID=0
            )

            user:UserProfile = UserProfile.objects.create(
                name=body['name'],
                accountType=body['accountType'],
                profilePicLink=body['profilePicLink'],
                identifier=identifier,
                favouriteWords=favs
            )
            favs.ownerID = user.id
            favs.save()
        return Response({'token':user.token,'user':UserProfileSerializer(user).data})