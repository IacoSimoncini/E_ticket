from django.urls import path
from . import views

urlpatterns = [
    path ('', views.events, name='home'),
    
    path ('contattaci', views.contattaci, name='contattaci'),
    path ('register/', views.registerPage, name='register'),
    path ('user/', views.userPage, name='user-page'),
    path ('manager/', views.managerPage, name='manager'),
    path ('login/', views.loginPage, name='login'),
    path ('logout/', views.logoutUser, name='logout'),
    path ('create_event/', views.createEvent, name='create_event'),
    path ('update_event/<str:pk>/', views.updateEvent, name='update_event'),
    path ('delete_event/<str:pk>/', views.deleteEvent, name='delete_event'),
    path ('user/buy_ticket/<str:pk>/', views.buyTicket, name='buy_ticket'),
    path ('reseller/', views.resellerPage, name='reseller-page'),
    path ('manage_ticket/<str:pk>/', views.manageTicket, name='manage_ticket'),
    path ('managebuy/<str:pk>/', views.manageBuy, name='managebuy'),
    path ('invalidate/<str:pk>/<str:id>/<str:ad>/', views.invalidateTicket, name='invalidate')
    
]


