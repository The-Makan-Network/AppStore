from django.contrib.auth.models import User
from .models import Loginteste

class MyAuthBackend:
    def authenticate(self, request, username=None, password=None):
        if username is None or password is None:
            # nothing to do
            return None

        # get 'User' object
        try:
            usr = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        # get 'Loginteste' object
        try:
            loginteste = Loginteste.objects.get(username=username)
        except Loginteste.DoesNotExist:
            return None

        # authenticate user
        if not loginteste.check_password(password):
            # incorrect password
            return None

        return usr

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            pass

        return None
