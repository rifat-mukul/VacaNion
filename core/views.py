from django.shortcuts import render,redirect
from .models import CustomUser, Hotel, Booked
from django.contrib import messages
from django.contrib.auth import login,get_user_model,authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime as dt



# Create your views here.
@login_required(login_url='signin')
def index(request):
    return render(request,'index.html')


@login_required(login_url='signin')
def tours(request):
    if request.method == "POST":
        print(request.POST)
        if request.POST['bookit'] is not None:
            name = request.POST['bookit']
            print('to book')
            return redirect('book',name)
        else:
            search = request.POST['search']
            if search == '':
                data = Hotel.objects.all()
            else:
                data = Hotel.objects.filter(Q(name__icontains=search)|Q(place__icontains=search))
    else:
        data = Hotel.objects.all()
    return render(request,'tours.html',{'hotels':data})

@login_required(login_url='signin')
def book(request,book_name):
    if not Hotel.objects.filter(name=book_name).exists():
        return redirect(tours)
    if request.method == "POST":
        hotel = Hotel.objects.get(name=book_name)
        user = CustomUser.objects.get(email=request.user.email)
        date = request.POST['crono']
        date_code = dt.datetime.strptime(date, "%Y-%m-%d").date()
        pnum = int(request.POST['pnum'])
        if pnum <= 0:
            messages.info(request,"Invalid person number")
            return render(request,'book.html',{'book_id':book_name,'pnum':pnum,'crono':date})
        if date_code <= dt.date.today():
            messages.info(request,"Invalid date")
            return render(request,'book.html',{'book_id':book_name,'pnum':pnum,'crono':date})
        if Booked.objects.filter(user=user,hotel=hotel,book_date=date_code).exists():
            messages.info(request,"Hotel already booked")
            return render(request,'book.html',{'book_id':book_name,'pnum':pnum,'crono':date})
        book_entry = Booked.objects.create(hotel=hotel,user=user,book_date=date_code,pnum=pnum)
        book_entry.save()
        return redirect(tours)
    return render(request,'book.html',{'book_id':book_name})

def addHotel(request):
    if request.method == "POST":
        name = request.POST['name']
        place = request.POST['place']
        price = request.POST['price']
        review = request.POST['review']

        info = {
                'name' : name,
                'price' : price,
                'review' : review,
                'place' : place
                }
        
        review = int(review)
        price = int(price)

        if review > 10 or review < 0:
            messages.info(request,"Bad reivew")
            return render(request,'addHotel.html',info)
        if price < 0:
            messages.info(request,"Bad price")
            return render(request,'addHotel.html',info)
        if Hotel.objects.filter(name = name).exists():
            messages.info(request,"Hotel name exists")
            return render(request,'addHotel.html',info)
        hotel = Hotel.objects.create(name = name,place = place,rating=review,price=price)
        hotel.save()
        return render(request,'addHotel.html',info)
    else:
        return render(request,'addHotel.html')

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        info  = {
            "email":email,
            'username': username,
            'password':password1,
            'password2':password2
        }

        if password1 != password2:
            messages.info(request,"Password do not match")
        
            return render(request,'signup.html',info)
        elif len(password1) <8:
            messages.info(request,"password should contain at least 8 character")

            return render(request,'signup.html',info)
        
        else:
            if CustomUser.objects.filter(email = email).exists():
                messages.info(request,'User email already exists')
                return redirect('signup')
            if CustomUser.objects.filter(username = username):

                messages.info(request,'Username already exists')
                return redirect('signup')
            user = CustomUser.objects.create_user(email = email,username=username,password = password1)
            user.save()

            return redirect(index)

    else:
        return render(request,'signup.html') #need  to create index def

def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # user = authenticate(request,email=email,password=password)



        if "@" in email:
            user = authenticate(request,email=email,password=password)
        else:
            if CustomUser.objects.filter(username = email).exists():

                user_obj = CustomUser.objects.filter(username = email)
                for user in user_obj:
                    access = user.email

                user = authenticate(request,email = access,password=password)
                print(user)
            else:
                user = None
        if user is not None:
            login(request,user)
            return redirect(tours)
        else:
            messages.info(request, 'Credential Invalid')
            return redirect('signin')
    else:
        return render(request,'signin.html')
    
@login_required(login_url='signin')
def signout(request):
    request.session.flush()
    return redirect(signin)

@login_required(login_url='signin')
def profile(request):
    if request.method == "POST":
        fname = request.POST["first-name"]
        lname = request.POST["last-name"]
        username = request.POST["username"]
        password = request.POST["password"]



    return render(request,'profile.html')


def changepass(request):
    if request.method == "POST":
        currentpass = request.POST['current-password']
        # user = CustomUser.objects.get(email = email)
    return render(request,'changepass.html')
