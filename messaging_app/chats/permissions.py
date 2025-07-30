from rest_framework.permissions import BasePermission


class IsOwnerOrParticipant(BasePermission):
    """
    Only allows access to the owner of a message/conversation or a participant.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'sender_id'):  # it's a Message
            return obj.sender_id == request.user or request.user in obj.conversation_id.participants.all()
        elif hasattr(obj, 'participants'):  # it's a Conversation
            return request.user in obj.participants.all()
        return False
