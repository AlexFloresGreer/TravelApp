from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import User, validationManager, Traveler, travelerManager
import bcrypt
import datetime
# from datetime import datetime

#CONTROLLER
#Create your views here.
def index(request):
    return render(request, 'beltexamapp/index.html')

def register(request):
    error = False
    if not validationManager().validateEmail(request, request.POST['email']):
        error = True

    if not validationManager().validateName(request, request.POST['first_name'], request.POST['last_name']):
        error = True
#convert bday
    if not validationManager().validateBirthday(request, request.POST['birthday']):
        error = True

    if not validationManager().validatePassword(request, request.POST['password'], request.POST['password_confirmation']):
        error = True

    if not error:
        hashed = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        user_info = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],birthday=request.POST['birthday'], password=hashed)
        user_info.save()
        # request.session['user'] = user_info.id
        messages.success(request, 'You have successfully been registered! Now you can login')
        return redirect('/')
    else:
        return redirect('/')

def login(request):
    user = validationManager().validateLogin(request, request.POST['email'], request.POST['password'])
    if user:
        request.session['user'] = request.POST['email']
        return redirect('/travels')
    else:
        return redirect('/')

def travels(request):
    # request.session['first_name']= request.POST['first_name']
    context = {
        'users' : Traveler.objects.filter(traveler__email=request.session['user']),
        'travelers' : Traveler.objects.exclude(traveler__email=request.session['user']),
        'joiners' : Traveler.objects.filter(creators__email=request.session['user'])
    }
    return render(request, 'beltexamapp/travels.html', context)

def add(request):
    return render(request,'beltexamapp/add.html')

#Create & validations
def create(request):
    error = False
    if not travelerManager().validateDestinationDescription(request, request.POST['destination'], request.POST['description']):
        error = True
    if not travelerManager().validateDates(request, request.POST['start_date'], request.POST['end_date']):
        error = True

    if not error:
        travelers = User.objects.get(email=request.session['user'])
        user_travel_info = Traveler.objects.create(destination=request.POST['destination'], description=request.POST['description'], start_date=request.POST['start_date'], end_date=request.POST['end_date'],traveler=travelers )
        user_travel_info.save()
        messages.success(request, 'Your trip has been registered!')
        return redirect('/travels')
    else:
        return redirect('/add')
    return render(request, 'beltexamapp/travels.html')

def join(request, id):
    trip= Traveler.objects.get(id=id)
    trip.creators.add(User.objects.get(email=request.session['user']))
    trip.save()
    return redirect('/travels')

def destination(request, id):
    context = {
        'traveler' : Traveler.objects.get(id=id),
    }
    print context
    return render(request,'beltexamapp/destination.html', context)

def logout(request):
    del request.session['user']
    return render(request,'beltexamapp/index.html')
