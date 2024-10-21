from django.urls import path
import apps.user.views as views  #importo todas las vistas que se encuentran en apps/user/views

app_name = 'user' #defino el nombre de la aplicacion 

urlpatterns = [
    path('users/profile/', views.UserProfileview.as_view(), name = 'user_profile'), #users/profile/ si pongo esto veo el html
    path('auth/register/',  views.RegisterView.as_view(), name = 'auth_register'), 
    path('auth/login/', views.LoginView.as_view() , name = 'auth_login'),
    path('auth/logout/',views.LogoutView.as_view(), name = 'auth_logout'),
]
