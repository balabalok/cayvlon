from django.urls import path
from . import views
urlpatterns = [
    path('', views.rate_, name='rate_manga'),
]