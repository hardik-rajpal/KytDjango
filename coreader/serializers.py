from rest_framework import serializers
from .models import *
class WordBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordBlock
        fields = '__all__'
    def to_representation(self, instance):
        repre = super().to_representation(instance)
        del repre['glossary']
        return repre
class GlossarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Glossary
        fields = '__all__'
    def to_representation(self, instance):
        repre = super().to_representation(instance)
        repre['words'] = WordBlockSerializer(WordBlock.objects.filter(glossary=instance),many=True).data
        return repre
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    # def to_representation(self, instance):
    #     repre =super().to_representation(instance)
    #     return repre
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
class FullBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    def to_representation(self, instance:Book):
        repre =  super().to_representation(instance)
        repre['glossaries'] = GlossarySerializer(Glossary.objects.filter(ownerType='book',ownerID=instance.id), many=True).data
        repre['notes'] = NoteSerializer(Note.objects.filter(book=instance),many=True).data
        return repre
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
    def to_representation(self, instance:UserProfile):
        repre =  super().to_representation(instance)
        repre['favouriteWords'] = GlossarySerializer(Glossary.objects.get(id=repre['favouriteWords'])).data
        del repre['token']
        return repre