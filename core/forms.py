from typing import Any, Mapping
from django.forms import ModelForm, TextInput, Select, PasswordInput, CharField, Form, CharField, DateInput, NumberInput, DateField, FileInput, ImageField, HiddenInput
from django.forms.renderers import BaseRenderer
from .models import CustomUser, Hotel, Booked, ChatTable, ReviewRating
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

class ProfileForm(ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','username','profileimg','password']

        widgets = {
            'username' : TextInput(attrs={"disabled":"True"}),
            'password' : PasswordInput(),
        }


    def clean_password(self):
        usrpass = self.cleaned_data.get('password')
        if not check_password(usrpass,self.instance.password):
            print("pass fkd")
            raise ValidationError("password did not match")

        return usrpass

class SubmitReview(ModelForm):

    class Meta:
        model = ReviewRating
        fields = ['ratings','review']

class UserTid(ModelForm):

    def __init__(self,*args,**kewargs):
        super().__init__(*args,**kewargs)
        self.fields['userTid'].label = "User Transaction ID"

    class Meta:
        model = Booked
        fields = ['userTid']


class OfficerTid(ModelForm):

    def __init__(self,*args,**kewargs):
        super().__init__(*args,**kewargs)
        self.fields['officerTid'].label = "Officer Transaction ID"

    class Meta:
        model = Booked
        fields = ['officerTid']


class CreateProfile(ModelForm):
    confirm_password = CharField(widget=PasswordInput())

    def __init__(self,*args,**kewargs):
        super().__init__(*args,**kewargs)
        self.fields['is_staff'].label = " Reservation Officer"

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','username','is_staff','profileimg','password']

        widgets = {
            'password' : PasswordInput(),
        }
        
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        cpassword = self.cleaned_data.get('confirm_password')

        if password != cpassword:
            raise ValidationError('passwords did not match.')

class HotelForm(ModelForm):
    def __init__(self,*args,**kewargs):
        super().__init__(*args,**kewargs)
        self.fields['hotelimg'].label = "Hotel image"
    
    class Meta:
        model = Hotel
        fields = ['place','name','price','hotelimg']
        
    
        widgets = {
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 0 or rating > 5:
            raise ValidationError('rating must be between 0 and 5.')
        return rating

class BookForm(ModelForm):
    date = DateField(widget=DateInput(attrs={"type":"date"}))
    pnum = CharField(widget=NumberInput(),label="People number")


    class Meta:
        model = Booked

        fields = ['date','pnum']


class ChangePassword(Form):
    old_password = CharField(widget=PasswordInput())
    new_password = CharField(widget=PasswordInput())
    confirm_password = CharField(widget=PasswordInput())

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args,**kwargs)

    def clean_old_password(self):
        opdata = self.cleaned_data.get('old_password')
        if not check_password(opdata,self.user.password):
            raise ValidationError("password did not match old password")
        return opdata

    def clean_confirm_password(self):
        opdata = self.cleaned_data.get('new_password')
        cpdata = self.cleaned_data.get('confirm_password')
        if not opdata == cpdata:
            raise ValidationError("password did not match with new password")
        return opdata



class SignIn(Form):
    username = CharField(widget=TextInput(attrs={"required":"true"}))
    password = CharField(widget=PasswordInput(attrs={"required":"true"}))



    def clean_username(self):
        usernamep = self.cleaned_data.get('username')
        if not CustomUser.objects.filter(username=usernamep).exists():
            raise ValidationError('username not found.')
        return usernamep

    def clean_password(self):
        usrname = self.cleaned_data.get('username')
        usrpass = self.cleaned_data.get('password')
        if not CustomUser.objects.filter(username=usrname):
            raise ValidationError('password did not match.')
        user = CustomUser.objects.get(username=usrname)
        if not check_password(usrpass,user.password):
            raise ValidationError('password did not match.')

        self.cleaned_data['user'] = user
        return usrpass

class ChatForm(ModelForm):
    class Meta:
        model = ChatTable

        fields = ['text']
    
class Reviewform(ModelForm):
    class Meta:
        model = ReviewRating

        fields = ['ratings']
    
    
