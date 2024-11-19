from django.urls import path
from . import views
from .views import advanced_report_view

urlpatterns = [
    path('', views.home, name='home'),  # Ana sayfa için URL
    path('physiotherapist/patients/', views.physiotherapist_patients, name='physiotherapist_patients'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/update/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/update/', views.appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('appointments/api/', views.appointment_api, name='appointment_api'),
    path('appointments/calendar/', views.calendar_view, name='calendar_view'),
    path('reports/', views.report_view, name='report_view'),
    path('reports/advanced/', advanced_report_view, name='advanced_reports'),
]
