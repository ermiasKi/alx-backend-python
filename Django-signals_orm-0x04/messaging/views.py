from .models import User

def delete_user(request, pk):
    user = User.objects.filter(pk=pk)
    user.delete()