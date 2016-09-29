from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User, UserManager
# Create your views here.

def index(request):
    return render(request, 'new_login/index.html')

def create_user(request):
    if request.method == 'POST':
        new_user = User.objects.createUser(request.POST)

        if new_user['created']:
            messages.success(request, new_user['new_user'].email + " was Successfully Registered, You May Login Now")
            return redirect('/')
        else:
            for error in new_user['errors']:
                messages.error(request, error)
            return redirect('/')

def login(request):
    if request.method =='POST':
        login = User.objects.login(request.POST)
        if login['loggedIn']:
            messages.success(request, "Welcome " + login['first_name'] + ", Successfully Logged In ")
            request.session['id'] = login['id']
            return redirect(reverse('books:index'))
            #return redirect('/success') old route
        else:
            for error in login['errors']:
                messages.error(request, error)
            return redirect('/')

def success(request):
    if "user_id" not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=request.session['id'])
    all_users = User.objects.all()
    context = {
        'users': all_users,
        'this_user': this_user
    }
    return render(request, 'new_login/loginsuccess.html', context)

def logOut(request):
    request.session.clear()
    return redirect('/')

def removeUser(request, id):
    result = User.objects.deleteUser(id)
    if result:
        return redirect('/success')
    else:
        print "User not Found"
