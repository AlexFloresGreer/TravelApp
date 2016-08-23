from django.conf.urls import url
from . import views                   #add this line

urlpatterns = [
  url(r'^$', views.index),  #this matches the "/" pathway
  url(r'^register$', views.register),
  url(r'^login$', views.login),
  url(r'^logout$', views.logout),
  url(r'^travels$', views.travels),
  url(r'^add$', views.add),
  url(r'^create$', views.create),
  url(r'^destination/(?P<id>\d+)/$', views.destination),
  url(r'^join/(?P<id>\d+)/$', views.join),


]
