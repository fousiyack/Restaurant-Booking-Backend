from rest_framework import serializers
from .models import Room, Message
from user_api.serializers import UsersSerializer

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'created_at','image')
        
        

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        author = UsersSerializer(source='author', read_only=True)
        print(author.data,"authorrrrrrrrrrr")
        model = Message
        fields = ('id', 'author', 'content', 'timestamp')
        