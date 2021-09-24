from .models import ChatSnippet
from rest_framework import serializers
class ChatSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSnippet
        fields = '__all__'