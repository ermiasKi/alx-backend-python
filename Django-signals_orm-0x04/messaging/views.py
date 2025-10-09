from .models import User

def delete_user(request, pk):
    cache_page = 60*1  # Cache for 1 minute
    user = User.objects.filter(pk=pk)
    user.delete()

def inbox(request):
    user = request.user

    messages = (
        Message.objects.filter(receiver=user)
        .select_related("sender", "receiver")  # optimize FK relationships
        .prefetch_related("replies")           # optimize reverse relationship
        .only("id", "sender__username", "content", "timestamp", "unread")
        .order_by("-timestamp")
    )