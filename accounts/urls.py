from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/',views.SignUpView.as_view(),name ='signup'),
    path('signup_success/', views.SignUpSuccessView.as_view(), name='signup_success'),

    path('home/',views.Home.as_view(),name='home'),
]