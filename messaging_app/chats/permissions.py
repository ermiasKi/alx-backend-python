from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if not request.user or not request.user.is_authenticated:
                return False
        # If obj is a Message, check the conversation's participants
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        # If obj is a Conversation, check its participants
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        return False