from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .permissions import IsParticipantOfConversation
from rest_framework.response import Response
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from .models import User, Message, Conversation
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        queryset = Message.objects.all()
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            queryset = queryset.filters(
                conversation__conversation_id=conversation_id)
        return queryset


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Conversation.objects.filter(participants__user_id=user_id)
        return Conversation.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        data = request.data.copy()
        data['conversation'] = conversation.conversation_id
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Respnose(serializer.data, status=status.HTTP_201_CREATED)
