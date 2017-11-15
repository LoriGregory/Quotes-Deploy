from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        if len(self.filter(email=post_data['email'])) > 0:
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')
        if errors:
            return errors
        return user
    def validate_registration(self, post_data):
        errors = []
        # check length of name fields
        if len(post_data['name']) < 2:
            errors.append("name fields must be at least 3 characters")
        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        # check uniqueness of email
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in use")
        # check password == password_confirm
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")
        if not errors:
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))
            new_user = self.create(
                name=post_data['name'],
                email=post_data['email'],
                password=hashed
            )
            return new_user
        return errors

class QuoteManager(models.Manager):
    def validate_post(self, post_data):
        errors = []
        # check length of name fields
        if len(post_data['name']) < 3:
            errors.append("name fields must be at least 4 characters")
        # check length of name message
        if len(post_data['quotes']) > 8:
            errors.append("quotes must be at least 10 characters") 
        

class User(models.Model):
    name = models.CharField(max_length=25)
    alias = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)
    objects = UserManager()
    def __str__(self):
        return self.name+' '+self.alias+' '+self.email

class Quote(models.Model):
    author = models.CharField(max_length=50)
    quotes = models.TextField(max_length=400)
    favorites_users = models.ManyToManyField(User, related_name = 'favorite_quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)
    objects = QuoteManager()
    
    def __str__(self):
        return self.author+' '+self.quotes
# class Favorite(models.Model):
#     Quote = models.ForeignKey(max_length=255)
#     Users = models.ManyToManyField(User, related_name="favority_quotes")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)



