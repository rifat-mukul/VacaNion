from django.contrib import admin
from .models import CustomUser, Hotel, Booked, Location, ChatTable

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Hotel)
admin.site.register(Booked)
admin.site.register(Location)
admin.site.register(ChatTable)
