from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entry/', views.vehicle_entry, name='vehicle_entry'),
    path('exit/', views.vehicle_exit, name='vehicle_exit'),
    path('reports/', views.reports, name='reports'),
    path('display/', views.display, name='display'),
    path('rates/', views.manage_rates, name='manage_rates'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('audit/', views.audit_log, name='audit_log'),

    path(
        'receipt/<int:payment_id>/',
        views.receipt,
        name='receipt'
    ),
]   