from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Books, Reviews, Authors, allManager
from ..new_login.models import User

# Create your views here.
def index(request):
    this_user = User.objects.get(id=request.session['id'])
    recent_reviews = Reviews.reviewMgr.all().order_by('-created_at')[:3]
    all_books = Books.bookMgr.all()
    all_authors = Authors.authorMgr.all()
    for i in recent_reviews:
        print i.created_at
    context={
        'this_user':this_user,
        'authors':all_authors,
        'recent_reviews': recent_reviews,
        'all_books': all_books
    }
    return render(request, 'bookRev/bookIndex.html', context)

def addForm(request):
    all_authors = Authors.authorMgr.all()
    print all_authors
    context = {
        'authors':all_authors
    }
    return render(request, 'bookRev/addBook.html', context)

def show(request, id):
    result = Books.bookMgr.get(id=id)
    reviews = Reviews.reviewMgr.filter(book=id)
    context = {
        'this_book': result,
        'all_reviews':reviews
    }
    return render(request, 'bookRev/show.html', context)

def user(request, id):
    result = User.objects.get(id=id)
    reviews = Reviews.reviewMgr.filter(user=id)
    print reviews
    context = {
        'this_user': result,
        "user_reviews": reviews
    }
    return render(request, 'bookRev/user.html', context)

def add_Book_Author_Review(request):
    if request.method == 'POST':
        #submits form info to validate all before adding entries
        manager = allManager()
        validateAll = manager.validateForm(request.POST)

        if validateAll['passed']:
            #adds each individual piece if they all pass
            user_id = request.session['id']
            new_author = Authors.authorMgr.addAuthor(request.POST)
            new_book = Books.bookMgr.addBook(request.POST)
            new_review = Reviews.reviewMgr.addReview(request.POST, user_id)
            messages.success(request, 'Book and Review successfully Logged')
            return redirect(reverse("books:index"))
        else:
            for error in validateAll['errors']:
                messages.error(request, error)
            return redirect('books:addForm')

def deleteReview(request):
    pass

def logOut(request):
    request.session.clear()
    return redirect(reverse('users:index'))

def addReview(request, id):
    user_id = request.session['id']
    if request.method == 'POST':
        new_Review = Reviews.reviewMgr.addReview(request.POST, user_id, id)
        messages.success(request, "Review successfully Added")
    #route paramater also requires 'id' which we passed (see show in urls.py)
    #TODO see how to do reverse with paramater
    return redirect(reverse('books:show', args=(id,)))
