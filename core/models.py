from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import CustomUserManager
from datetime import datetime

# Create your models here.

class CustomUser(AbstractBaseUser,PermissionsMixin,models.Model):
    email = models.EmailField(max_length=100,unique=True,primary_key = True)
    username = models.CharField(max_length=100,unique=True)
    profileimg = models.ImageField(upload_to="profileimg",default="blank-profile-picture.png",blank=True)
    password = models.CharField(max_length = 100)
    first_name = models.CharField(max_length=20,blank=True,null=True)
    last_name = models.CharField(max_length=20,blank=True,null=True)

    has_joined = models.DateField(default = datetime.now)  

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email 

class Location(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class Hotel(models.Model):
    place = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=20,blank=True,null=True)
    price = models.IntegerField()
    rating= models.FloatField(default=10)
    hotelimg = models.ImageField(upload_to="hotelimg",default="blank-hotel-picture.png")
    officer = models.ForeignKey(CustomUser,on_delete=models.CASCADE,limit_choices_to={'is_staff': True})

    def __str__(self):
        return self.name

class Booked(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    book_date = models.DateField(default = datetime.now)  
    pnum = models.IntegerField(default=1)
    userTid = models.IntegerField(default=0)
    officerTid = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + " -> " + self.hotel.name + "@" + str(self.book_date)

class ChatTable(models.Model):
    booking = models.ForeignKey(Booked,on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

class ReviewRating(models.Model):
    hotel = models.OneToOneField(Booked,on_delete=models.CASCADE)
    ratings = models.FloatField()
    review = models.TextField()

    def save(self,*args,**keargs):
        res = super().save(*args,**keargs)
        reviews = ReviewRating.objects.filter(hotel__hotel=self.hotel.hotel)
        n = reviews.count()
        sum = 0
        for review in reviews:
            sum += review.ratings
        print(sum/n,"========",reviews)
        tpl = self.hotel.hotel
        tpl.rating = sum/n
        tpl.save()


    def __str__(self):
            return f"{self.hotel} -> {self.ratings} - {self.review}"
