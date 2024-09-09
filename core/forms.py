from django.forms import ModelForm, TextInput, CharField, PasswordInput
from .models import CustomUser

class ProfileForm(ModelForm):
    confirm_password = PasswordInput()
    
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','username','profileimg','password']

        widgets = {
            'username' : TextInput(attrs={"disabled":"True"}),
            'password' : PasswordInput(),
        }


