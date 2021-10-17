from .models import ChatSnippet
from rest_framework import serializers
alias = {
    'Sourish Wockrell':'The Bear',
    'Srikar rockwell New':'The Giraffe',
    '+1 (385) 296-8922':'The Koala',
    'Hardik Rajpal':'The Tiger',
    'Sourish Sengupta':'The Bear',
    'Vijay Kiran Satyam':'The Koala',
    'Srikar':'The Giraffe',
    '+1 (408) 315-5405':'The Elephant'
}
class ChatSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSnippet
        fields = '__all__'
    def to_representation(self, instance):
        repre =  super().to_representation(instance)
        for key in alias:
            repre['snippet'] = repre['snippet'].replace(key, alias[key])
        if(repre['published']):
            return repre
        else:
            repre['snippet'] = "abc"
            return repre