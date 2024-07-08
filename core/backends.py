from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User_model = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self,request,email=None,password = None,**kwargs):
        if email is None and password in None:
            return None
        try:
            user = User_model.objects.get(email = email)
            if user.check_password(password):
                return user
        except User_model.DoesNotExist:
            return None
        return None
            
        