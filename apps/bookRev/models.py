from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from ..new_login.models import User

class allManager(models.Manager):
    #must handle all validations in one
    #since we only want entries to be created in the DB if
    #ALL pass, THEN route to respective addfunctions and return
    #IMPORTANT: get returns error if it can't find, filter returns array
    def validateForm(self, data):
        errors = []
        response = {}
        #author validation
        if len(data['author_name']) < 1:
            errors.append("Must add an Author")

        existing_author = Authors.authorMgr.filter(name=data['author_name'])
        #filter returns array, empty array is 'falsey', thus if not 'falsey'
        # returns True, else if not 'true' (true means array has stuff)
        if existing_author:
            errors.append("Author already exists, Select from Menu")

        #book validation
        if len(data['title']) < 1:
            errors.append("Book Title Cannot be Blank!")
        existing_book = Books.bookMgr.filter(title=data['title'])
        if existing_book:
            errors.append("Book already exists, add a new Review")

        #Review Validation
        if len(data['review']) < 1:
            errors.append("Review Cannot Be Blank!")
        #done validations, if errors, return errors, else create entries
        if len(errors) > 0:
            response['passed'] = False
            response['errors'] = errors
            return response
        else:
            response['passed'] = True
            return response

    def addAuthor(self, data):
        new_author = self.create(name=data['author_name'])
        return new_author

    def addBook(self, data):
        author = Authors.authorMgr.get(name=data['author_name'])
        new_book =self.create(title=data['title'], author=author)
        return new_book

    def addReview(self, data, user_id, book_id):
        print data
        print book_id
        print user_id
        #user_id is request.session['user_id'] from views
        book = Books.bookMgr.get(id=book_id)
        user = User.objects.get(id=user_id)
        new_review = self.create(review=data['review'], rating=data['rating'], book=book, user=user)
        return new_review

    # def addAnotherReview(self, data, user_id):
    #     book = Books.bookMgr.get(id=data['book_id'])
    #     user = User.objects.get(id=user_id)
    #     new_review = Reviews.reviewMgr.create(review=data['add_review'], rating=data['rating'], book=book, user=user)
    #     return new_review

# Create your models here.
class Authors(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    authorMgr = allManager()

class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Authors)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bookMgr = allManager()

class Reviews(models.Model):
    review = models.TextField(max_length=1000)
    rating = models.IntegerField()
    book = models.ForeignKey(Books, related_name="userBooks")
    user = models.ForeignKey(User, related_name= "userReviews")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewMgr = allManager()
