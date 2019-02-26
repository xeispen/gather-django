from rest_framework import serializers
from gather_api.models import Node, User, Connection, Message

class UserSerializer(serializers.HyperlinkedModelSerializer):
    #node = serializers.HyperlinkedRelatedField(many=True, view_name='node-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'social_id','profile_pic')
        extra_kwargs = {'username': {'required': False}, 'password': {'required': False}}

class NodeSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Node
        fields = ('id', 'uuid', 'minor', 'major', 'device_name', 'device_token', 'created', 'owner', 'userid')


class ConnectionSerializer(serializers.HyperlinkedModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Connection
        fields = ('source', 'destination', 'waved', 'created', 'updated')


# Message Serializer
class MessageSerializer(serializers.HyperlinkedModelSerializer):
    """For Serializing Message"""
    sender = serializers.SlugRelatedField(many=False, slug_field='id', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='id', queryset=User.objects.all())
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
