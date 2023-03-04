from django.contrib.auth.backends import ModelBackend
from AppOko.models import CustomUser
from django.contrib.auth.hashers import check_password 


class PasswordlessAuthBackend(ModelBackend):
    def authenticate(request, self, username, password):
        try:
            user = CustomUser.objects.get(username=username)
            print(user)
            if user.user_type == '4':
                if username == username and password == password:
                    return user
                return None
            elif user.user_type == '1':
                if user.check_password(password):
                    return user
                return None
            return None
        except CustomUser.DoesNotExist:
            return None
    def get_user(request, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
