from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name ='index'),
    path('signup/',views.signup,name="signup"),
    path('signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),
    path('tours/',views.tours,name='tours'),
    path('profile/',views.profile,name='profile'),
    path('changepass/',views.changepass,name='changepass'),
    path('addHotel/',views.addHotel,name='addhotel'),
    path('book/<int:book_id>/',views.book,name='book'),
    path('chat/<int:book_id>/',views.chat,name='chat'),
    path('analytics/',views.analytics,name="analytics"),
    path('reviw/<int:book_id>',views.review,name="review"),
    path('delete/<int:book_id>',views.deleteBooking,name="dBook"),
]
