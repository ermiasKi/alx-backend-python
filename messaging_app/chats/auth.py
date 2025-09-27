from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


def user_authenticate(data):
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = authenticate(username=username, password=password)

        # if user is None:
        #     raise ValidationError('invalid credentials')
        return user