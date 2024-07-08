from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self,request,email=None,password = None,**kwargs):
        if email is not None:
            email = kwargs.get(UserModel.USERNAME_FIELD)
        if email is None or password is None:
            return
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        
        else:
            if user.check_password(password):
                return user
        return None
    
