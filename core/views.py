from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import login,get_user_model,authenticate


# Create your views here.
def index(request):
    return render(request,'index.html')

def tours(request):
    return render(request,'tours.html')

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # info  = {
        #     "email":email,
        #     'username': username,
        #     'password':password1
        # }

        if password1 != password2:
            messages.info(request,"Password do not match")
        
            return render(request,'signup.html')#,info)
        elif len(password1) <8:
            messages.info(request,"password should contain at least 8 character")

            return render(request,'signup.html')#,info)
        
        else:
            if CustomUser.objects.filter(email = email).exists():
                messages.info(request,'User email already exists')
                return redirect('signup')
            user = CustomUser.objects.create(email = email,username=username,password = password1)
            user.set_password(password1)
            user.save()

            return redirect(index)

    else:
        return render(request,'signup.html') #need  to create index def

def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # if CustomUser.objects.filter(email = email).exists():
        #     user = authenticate(request,email=email,password=password)
        # else:
        #     user = None
        user = authenticate(request,email = email,password = password)
        
                
        if user is not None:
            login(request,user)
            return redirect(tours)
        else:
            messages.info(request,"Credintial invalid")
            return redirect(signin)
            
    else:
        return render(request,'signin.html')
