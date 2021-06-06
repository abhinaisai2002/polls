from django.contrib import admin
from django.urls import path
from . import views
app_name = 'polls'
urlpatterns = [
    path('allpolls/',views.polls_view,name='allpolls')
]