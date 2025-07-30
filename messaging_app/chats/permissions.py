from rest_framework.permissions import BasePermission
from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access or modify it.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # `obj` will be a Message or Conversation instance
        user = request.user

        # For messages, check if the user is a participant in the conversation
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()

        # For conversation objects
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        return False
