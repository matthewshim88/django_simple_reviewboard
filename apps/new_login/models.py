from __future__ import unicode_literals
import re, bcrypt
from django.db import models

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def createUser(self, data):
        response = {}
        errors = self.validateRegister(data)
        if len(errors) > 0:
            response['created'] = False
            response['errors'] = errors
        else:
            password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            new_user = self.create(first_name = data['fname'], last_name = data['lname'], alias = data['alias'], email = data['email'], password=password)
            response['created'] = True
            response['new_user'] = new_user
        return response

    def login(self, data):
        response = {}
        errors = self.validateLogin(data)
        #IMPORTANT: .GET works if there is one record that matches,
        # if there are 0 or more than one, .GET returns an error
        #return user with the email password
        if len(errors) > 0:
            response['loggedIn'] = False
            response['errors'] = errors
            return response
        else:
            user_login = User.objects.get(email=data['email'])
            password_hash = bcrypt.hashpw(data['password'].encode(), user_login.password.encode())
            response['loggedIn'] = True
            response['id'] = user_login.id
            response['first_name'] = user_login.first_name
            response['created'] = True
            return response

    def deleteUser(request, id):
        e = User.objects.get(id=id)
        if not e:
            return False
        else:
            e.delete()
            return True

    #helper methods to validate info
    def validateRegister(self, data):
        errors = []
        if len(data['fname']) < 2 or len(data['lname']) < 2:
            errors.append("First and Last names must be at least 2 Characters")
        if len(data['password']) < 8:
            errors.append("Password Must be at least 8 Characters")
        if not data['fname'].isalpha() or not data['lname'].isalpha():
            errors.append("First and Last name can only be letters")
        if len(data['alias']) < 2:
            errors.append("User Alias must be at least 2 Characters")
        if data['password'] != data['confirmpass']:
            errors.append('Confirm Password does not match')

        existing_email = self.filter(email = data['email'])
        if existing_email:
            errors.append('Submitted Email already exists in the Database')
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Not a Valid Email, Please Try Again")
        return errors

    def validateLogin(self, data):
        errors = []

        if len(data['email']) < 2:
            errors.append("Email cannot be blank")
        if len(data['password']) < 8:
            errors.append("Password is Invalid/Doesn't Match")
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Invalid Email")
        #checks for existing email, if doesn't, breaks and returns error
        existing_user = self.filter(email=data['email'])
        if not existing_user:
            errors.append("User doesn't exist, please Register")
            return errors
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
