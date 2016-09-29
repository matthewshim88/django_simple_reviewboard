from django.conf.urls import url
from . import views
from views import index, create_user, login, success, removeUser, logOut

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^register$', create_user, name='create_user'),
    url(r'^login$', login, name='login'),
    url(r'^success$', success, name='success'),
    url(r'^logout$', logOut, name='logOut'),
    url(r'^selectAccount/(?P<id>[0-9]*)/delete', removeUser, name='removeUser')
]
