from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_2, name='home'),
    path('manga/<str:m_slug>/', views.manga_info, name='minfo'),
    path('reader/<str:c_slug>/', views.chapter_read, name='c_read'),
    path('search/', views.search, name='search'),
    path('browse/', views.browse, name='browse'),
    path('shine/<str:slug>', views.shine, name='shine'),

]
