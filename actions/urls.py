from django.urls import include, path
from . import views
urlpatterns = [
    path('events/', views.events, name='events'),
]