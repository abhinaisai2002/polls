from django.contrib import admin
from django.urls import path
from . import views
app_name = 'polls'
urlpatterns = [
    path('allpolls/', views.polls_view, name='allpolls'),
    path('allpolls/<str:id>/', views.poll_view, name='poll'),
    path('submitpoll/', views.submit_poll_view, name='submit_poll'),
    path('getpolldata/',views.get_poll_data,name='getpolls'),
    path('toppolls/',views.top_polls,name='toppolls'),
    path('comment/', views.comment_view, name='comment'),
    path('searchpoll/',views.search_view,name='search'),
]

handler404 = 'macro_project.views.no_page_found'