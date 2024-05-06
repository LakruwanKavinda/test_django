from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('upload-pdf/', views.upload_pdf_view, name='upload_pdf'),
    path('search/', views.search_pdf, name='search_pdf'),
    path('pdf/<int:pdf_id>/', views.view_pdf,
         name='view_pdf'),  # Add this line
    path('', views.getRoutes),
]
