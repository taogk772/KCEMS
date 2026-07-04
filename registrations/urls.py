from django.urls import path
from . import views

urlpatterns = [
    path('<int:event_id>/', views.register, name='register'),
    path('receipt/pdf/<int:pk>/', views.download_receipt_pdf, name='receipt_pdf'),
    path('registrations/verify/<str:reg_number>/', views.verify_registration, name='verify_registration'),
    path('verify/<str:reg_number>/', views.verify_registration, name='verify'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('success/<int:pk>/', views.registration_success, name='registration_success'),
]