from django.shortcuts import render,redirect
from .models import  Hotel, Booked, ChatTable, CustomUser
from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, HotelForm, CreateProfile, SignIn, BookForm, ChangePassword, ChatForm
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime as dt


# Create your views here.
@login_required(login_url='signin')
def index(request):
    if not request.user.is_staff:
        shows = Booked.objects.filter(user=request.user)
    else:
        hotels = Hotel.objects.filter(officer=request.user)
        print(hotels)
        shows = Booked.objects.filter(hotel__in=hotels)
    context = {
        'books' : shows,
    }
    return render(request,'index.html',context)

def test(request):
    return render(request,'test.html')

@login_required(login_url='signin')
def analytics(request):
    month_count = {(id+1):Booked.objects.filter(book_date__month=(id+1)).count()  for  id in range(12)}
    user_staff_radio = {}
    user_staff_radio['user'] = CustomUser.objects.filter(is_staff=False).count()
    user_staff_radio['officer'] = CustomUser.objects.filter(is_staff=True).count()

    context = {
        "month_count": month_count,
        "us_ratio"   : user_staff_radio,
    }

    return render(request,"analytics.html",context)

@login_required(login_url='signin')
def chat(request,book_id):
    booking = get_object_or_404(Booked,id=book_id)
    if request.method == "POST":
        form = ChatForm(request.POST,request.FILES,initial={"booking":booking,"sender":request.user})
        #print(form.errors)
        if form.is_valid():
            txt = form.save(commit=False)
            txt.booking = booking
            txt.sender = request.user
            txt.save()

    else:
        form = ChatForm(initial={"booking":booking,"sender":request.user})


    texts = ChatTable.objects.filter(booking=booking)

    texts.reverse()


    context = {
        'form' : form,
        'name' : booking.hotel.name,
        'action' : 'Send',
        'chat' : texts,
    }
    return render(request,'chat.html',context)


@login_required(login_url='signin')
def tours(request):
    if request.method == "POST":
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
def book(request,book_id):
    hotel = get_object_or_404(Hotel,id=book_id)
    print(hotel)
    if request.method == "POST":
        form = BookForm(request.POST,request.FILES)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.hotel = hotel
            booking.save()
    else:
        form = BookForm()

    context = {
        'form': form,
        'action': 'Book',
        'name' : 'Book Hotel',
    }

    return render(request,'baseform.html',context)

def addHotel(request):
    if request.method == "POST":
        form = HotelForm(request.POST,request.FILES)

        if form.is_valid():
            usr = form.save(commit=False)
            usr.officer = request.user
            usr.save()
            return redirect(index)
    else:
        form = HotelForm()

    context = {
        'form': form,
        'action': 'Add',
        'name' : 'Add hotel',
    }

    return render(request,'baseform.html',context)


def signup(request):
    if request.method == 'POST':
        form = CreateProfile(request.POST,request.FILES)
        if form.is_valid():
            usr = form.save()
            usr.set_password(form.cleaned_data['password'])
            usr.save()
            return redirect(signin)
    else:
        form = CreateProfile()
    context = {
        'form': form,
        'action': 'Sign up',
        'name' : 'Sign Up',
    }
    return render(request,'baseform.html',context)

def signin(request):
    if request.method == 'POST':
        form = SignIn(request.POST,request.FILES)
        if form.is_valid():
            userdata = form.cleaned_data['user']
            user = authenticate(request,email = userdata.email,password=form.cleaned_data['password'])
            login(request,user)
            return redirect(index)
    else:
        form = SignIn()
    context = {
        'form': form,
        'action': 'Sign up',
        'name' : 'Sign Up',
    }
    return render(request,'baseform.html',context)
    
@login_required(login_url='signin')
def signout(request):
    request.session.flush()
    return redirect(signin)


@login_required(login_url='signin')
def profile(request):
    errors = {}
    user = request.user

    if request.method == "POST":
        updated_data = request.POST.copy()
        updated_data.update({'username': user.username})
        form = ProfileForm(updated_data,request.FILES,instance=user)

        last_pass = request.user.password
        if not form.is_valid():
            errors = {key:value[0] for key,value in form.errors.items()}
        elif not check_password(form.cleaned_data['password'],last_pass):
            errors = {'password': 'did not match'}
        else:
            usr = form.save()
            usr.set_password(form.cleaned_data['password'])
            usr.save()
            return redirect(signin)
    form = ProfileForm(instance=user,initial={"password":""})

    context = {
        'form': form,
        'messages': errors,
        'action': 'Save Changes',
        'name' : 'Edit Profiler',
    }

    return render(request,'baseform.html',context)


def changepass(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST,request.FILES,user=request.user,)
        if form.is_valid():
            
            print(form.cleaned_data)
    else:
        form = ChangePassword(user=request.user)
    context = {
        'form': form,
        'action': 'Change password',
        'name' : 'Change Password',
    }
    return render(request,'baseform.html',context)


#by mukul

def tours(request):

    search_query = request.GET.get('search', '')

    if search_query:
        tours = Hotel.objects.filter(place__icontains=search_query) | Hotel.objects.filter(name__icontains=search_query)
    else:
        tours = Hotel.objects.all()

    context = {
        'tours': tours,
        'search_query': search_query  
    }

    return render(request, 'tours.html', context)
