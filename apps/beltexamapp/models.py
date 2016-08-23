from __future__ import unicode_literals
from django.db import models
import re
from django.contrib import messages
import bcrypt
from datetime import datetime, date, timedelta, time
from time import strftime
# Create your models here.
class validationManager(models.Manager):
    def validateEmail(self, request, email):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')
        if not EMAIL_REGEX.match(email):
            messages.error(request, "Email is not valid")
            return False
        else:
            # check if email is already in database
            try:
                User.objects.get(email=email)
                messages.error(request, "Email is already in use")
                return False
            except User.DoesNotExist:
                pass
        return True

    def validateName(self, request, first_name, last_name):
        no_error = True
        if len(first_name) < 2 or any(char.isdigit() for char in first_name):
            messages.error(request, 'Frist name must be 2 characters and only letters')
            no_error = False
        if len(last_name) < 2 or any(char.isdigit() for char in last_name):
            messages.error(request, 'Last name must be 2 characters and only letters')
            no_error = False
        return no_error

    def validateBirthday(self, request, birthday):
        no_error = True
        now = strftime('%Y-%m-%d')
        if request.POST['birthday'] == "":
            messages.error(request, 'Birthday can not be blank')
            no_error = False
        if request.POST['birthday'] > now:
            messages.error(request, 'Birthday can not be in the future')
            no_error = False
        return no_error

    def validatePassword(self, request, password, confirm_password):
        no_error = True
        if len(password) < 8:
            messages.error(request, 'Password must be greater than 8 characters')
            no_error = False
        if not password == confirm_password:
            messages.error(request, 'Password confirmation must match password')
            no_error = False
        return no_error

    def validateLogin(self, request, email, password):
        try:
            user = User.objects.get(email=email)
            if bcrypt.hashpw(password.encode('utf-8'), user.password.encode('utf-8')) == user.password:
                messages.success(request, "You've been logged in!")
                return (True, user.first_name, user.id)
        except User.DoesNotExist:
            messages.error(request, "Invalid email")
            return False

class travelerManager(models.Manager):
    def validateDestinationDescription(self, request, destination, description):
        no_error = True
        if len(destination) < 2 or any(char.isdigit() for char in destination):
            messages.error(request, 'Destination must be greater than 2 characters and only letters')
            no_error = False
        if len(description) < 2 or any(char.isdigit() for char in description):
            messages.error(request, 'Description must be greater than 2 characters and only letters')
            no_error = False
        return no_error

    def validateDates(self, request, start_date, end_date):
        no_error = True
        now = strftime('%Y-%m-%d')
        if request.POST['start_date'] and request.POST['end_date']== "":
            messages.error(request, 'Travel dates can not be blank')
            no_error = False
        if request.POST['start_date'] < now:
            messages.error(request, 'Travel Date From must be in the future')
            no_error = False
        if request.POST['end_date'] < now:
            messages.error(request, 'Travel Date To must be in the future')
            no_error = False
        if request.POST['end_date'] < request.POST['start_date']:
            messages.error(request, 'Travel Date From can not be after Travel Date To!')
            no_error = False
        return no_error

#creator
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    birthday = models.DateField(null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    emailManager = validationManager()
    objects = models.Manager()

#models.TextField()
#user_id = models.ForeignKey(User)

#traveler
class Traveler(models.Model):
    creators = models.ManyToManyField(User, related_name='creator')
    traveler = models.ForeignKey(User)
    destination = models.CharField(max_length=45, blank=False)
    start_date = models.DateField( null=False, blank=False )
    end_date = models.DateField(null=False, blank=False )
    description = models.CharField(max_length=45,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    travelerManager = travelerManager()
    objects = models.Manager()
