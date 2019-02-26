from gather_api.models import User, Node, Connection, Message
from gather_api.serializers import NodeSerializer, UserSerializer, ConnectionSerializer, MessageSerializer
from gather_api.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.pagination import PageNumberPagination
import gather_api.apns as apns
import sys
import json
import social_django

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'], detail=True)
    def perform_create(self, serializer):
        if serializer.is_valid():
            print("creating user")
            user = User.objects.create_user(serializer.data['username'])
            #user.social_id = serializer
            user.set_password(serializer.data['password'])
            #social = self.get_social_auth()
            #print(social.social_id)
            user.save()
            return Response({'status': 'user created'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NodeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        filtered_users = self.queryset.filter(owner=self.request.user)
        #TODO: Add function to check if node already exists for that users
        if len(filtered_users) == 0:
            print("USER DOES NOT HAVE NODE IN DB")
            serializer.save(owner=self.request.user)
        else:
            print("USER ALREADY HAS NODE IN DB")
            serializer.instance = filtered_users[0]
            serializer.save()
            # TODO: Add some sort of cleanup functon


    def get_queryset(self):
        queryset = Node.objects.all()
        minor = self.request.query_params.get('minor')
        major = self.request.query_params.get('major')

        if minor is not None and major is not None:
            queryset = queryset.filter(minor=minor, major=major)
            # Make sure we get the node before anything
            if len(queryset) == 1:
                print("Returning node!!!!!!!!")
                # Call a class function for connection to create a new object
                # Get my own node
                try:
                    # TODO: Refactor into a Connection class function
                    user = self.request.user
                    source_node = Node.objects.get(owner=user)
                    connection = Connection.objects.filter(source=source_node, destination=queryset[0])
                    if len(connection) == 0:
                        # Create connection object
                        connection = Connection.objects.create(source=source_node, destination=queryset[0])
                        connection.save()
                        print("New connection created")
                    else:
                        print("Connection already exists")
                except Node.DoesNotExist:
                    print("Does not exist")
        return queryset


    @action(methods=['post'], detail=True)
    def sendapns(self, request, pk=None):
        try:
            user = self.request.user
            dest_node = Node.objects.get(pk=pk)
            source_node = Node.objects.get(owner=user)
            # Update Connection (might want to refactor this too)
            queryset = Connection.objects.filter(source=source_node, destination=dest_node)
            if len(queryset) == 1:
                print("Setting Connection.waved to true")
                queryset[0].waved = True
                queryset[0].save()
            # Pass device token to apns
            token = dest_node.device_token
            apns.post(token)
        except Node.DoesNotExist:
            print("DOES NOT EXIST")
        return Response({'status': 'notifcation sent!'})


class ConnectionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


    def get_queryset(self):
        queryset = Connection.objects.all()
        source = self.request.query_params.get('source')
        destination = self.request.query_params.get('destination')

        if source is not None and destination is not None:
            queryset = queryset.filter(source=source, destination=destination)
            # Make sure we get the node before anything
            if len(queryset) == 1:
                print("Returning Connection!!!!!!!!")
                # Call a class function for connection to create a new object
                # Get my own node
        return queryset



class MessageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def get_queryset(self):
        queryset = Message.objects.all()
        sender = self.request.query_params.get('sender')
        receiver = self.request.query_params.get('receiver')

        if sender is not None and receiver is not None:
            queryset = queryset.filter(sender=sender, receiver=receiver) | queryset.filter(sender=receiver, receiver=sender)
        return queryset

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):

        if serializer.is_valid():
            serializer.save()

            queryset = Node.objects.all()
            filtered_nodes = queryset.filter(userid=serializer.data["receiver"])

            token = filtered_nodes[0].device_token


            apns.post(token)

            return Response({'status': 'message created'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
