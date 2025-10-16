from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('universities/', views.universities, name='universities'),
    path('colleges/', views.colleges, name='colleges'),
    path('roadmap/', views.roadmap, name='roadmap'),
    path('analytics/', views.analytics, name='analytics'),
]