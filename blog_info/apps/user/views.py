#from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView as LoginViewDjango , LogoutView as LogoutViewDjango
from django.contrib.auth.models import Group
from django.urls import reverse_lazy

# pueba
from django.contrib.auth import authenticate , login
from django.shortcuts import redirect

from apps.user.forms import RegisterForm , LoginForm

# Create your views here. aca se crean las views , las vistas

class UserProfileview (TemplateView):
    template_name = 'user/user_profile.html' #este es el templete / html que utiliza la vista (que se encuentre en templete/user)

class RegisterView (CreateView):
    template_name = 'auth/auth_register.html' # crear el templete
    form_class = RegisterForm
    success_url = reverse_lazy('home') # redirecciona al home una vez registrado el usuario
    
    def form_valid(self, form): 
        # Llama a la función form_valid de la clase padre y guarda el usuario 
        response = super().form_valid(form) 
        # Asignar el grupo Registered al usuario recién creado 
        registered_group = Group.objects.get(name='Registereds') 
        self.object.groups.add(registered_group) 
        # En caso de ser necesario se le puede asignar explicitamente los permisos del grupo al usuario 
        # for permission in registered_group.permissions.all(): 
        #     self.object.user_permissions.add(permission) 

        #Autenticar el usuario despues del registro
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username= username, password= password)

        if user is not None:
            login(self.request, user) # Iniciamos sesion del usuario
            return redirect(self.get_success_url()) #'home'
        
        return response 

class LoginView (LoginViewDjango):
    template_name = 'auth/auth_login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        return reverse_lazy('home')
    


class LogoutView(LogoutViewDjango):
    next_page = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')