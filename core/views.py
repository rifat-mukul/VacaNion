from django.shortcuts import render,redirect
from .models import CustomUser, Hotel
from django.contrib import messages
from django.contrib.auth import login,get_user_model,authenticate
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required(login_url='signin')
def index(request):
    return render(request,'index.html')


@login_required(login_url='signin')
def tours(request):
    return render(request,'tours.html')

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
            user = CustomUser.objects.create(email = email,username=username,password = password1)
            user.set_password(password1)
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
