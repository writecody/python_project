from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def RegValidator(request, postData):
        print(postData)
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Name should be at least 2 letters."
        elif str.isalpha(postData['name']) == False:
            errors['name'] = "Name should only contain letters."
        if len(postData['username']) < 6:
            errors['username'] = "Enter a valid username."
        try:
            User.objects.get(username=postData['username'])
            errors['username'] = "This username is taken."
        except:
            print('Error: username already exists.')
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters."
        if postData['confirm'] != postData['password']:
            errors['confirm'] = "Passwords do not match."
        return errors

    def LoginValidator(request, postData):
        print(postData)
        errors = {}
        user = User.objects.get(username = postData['username'])
        if not user:
            errors['no_user'] = "Username does not exist."
            return errors
        if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            print("password match")
            return errors
        else: 
            errors['invalid_login'] = "Password does not match for this user."
        return errors

class User(models.Model):
    name = models.CharField(max_length=25)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    confirm = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class WishManager(models.Manager):
    def WishValidator(request, postData):
        print(postData)
        errors = {}
        wish = Wish.objects.filter(item=postData['item'])
        if len(postData['item']) < 3:
            errors['item'] = "Item name must have at least three characters."
        return errors

class Wish(models.Model):
    item = models.CharField(max_length=25)
    creator = models.ForeignKey(User, related_name="created_by", default=0)
    date_added = models.DateTimeField(auto_now_add = True)
    savers = models.ManyToManyField(User, related_name="saved_by", default=0)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = WishManager()

        