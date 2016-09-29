from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^books$', views.index, name ='index'),
    url(r'^show/(?P<id>\d+)$', views.show, name='show'),
    url(r'^user/(?P<id>\d+)$', views.user, name='user'),
    url(r'^addForm$', views.addForm, name='addForm'),
    url(r'^logOut$', views.logOut, name='logOut'),
    url(r'^addBook$', views.add_Book_Author_Review, name='newBook'),
    url(r'^addReview/(?P<id>\d+)$', views.addReview, name='addReview'),
]
