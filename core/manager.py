from typing import Any
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_field):
        if not email:
            raise ValueError("Provide a valid email")
        email = self.normalize_email(email)
        user = self.model(email = email,**extra_field)
        user.set_password(password)
        user.save(using = self.db)

        return user
    
    def create_superuser(self,email,password,**extra_field):
        extra_field.setdefault("is_superuser",True)
        extra_field.setdefault("is_staff",True)

        return self.create_user(email,password,**extra_field)