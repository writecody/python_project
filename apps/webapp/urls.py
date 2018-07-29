from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^new', views.new),
    url(r'^add/(?P<id>\d+)$', views.add),
    url(r'^create', views.create),
    url(r'^dashboard', views.dashboard),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^saved/(?P<id>\d+)$', views.saved),
    url(r'^delete/(?P<id>\d+)$', views.delete),
]
