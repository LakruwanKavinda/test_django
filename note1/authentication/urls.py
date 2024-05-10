from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('search_pdf/', views.search_pdf, name='search_pdf'),
]
