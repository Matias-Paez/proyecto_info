from typing import Any
from django import forms 
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm 

from apps.user.models import User 

# creo aqui los formularios -- aqui van a ir todos los formularios --CRUD
#Formulario de Update

# Formulario para resgistro de un usuario
class RegisterForm(UserCreationForm): #UserCreationForm 
    class Meta: 
        model = User 
        fields = ('first_name','last_name','username', 'email','password1','password2' ,'alias', 'avatar') #datos que voy a pedir para registrar un usuario

    first_name= forms.CharField(label="Nombre", max_length=40,
                                widget= forms.TextInput(attrs={
                                    'class': 'w-full px-3 py-2 mt-1 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                                    'placeholder': 'Ingresa tu nombre'}))
    
    last_name = forms.CharField(label="Apellido", max_length=30, 
                                widget=forms.TextInput(attrs={
                                    'class': 'w-full px-3 py-2 mt-1 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                                    'placeholder': 'Ingresa tu apellido'}))
    
    username = forms.CharField(label="Nombre de Usuario", max_length=150, 
                               widget=forms.TextInput(attrs={        
                                   'class': 'w-full px-3 py-2 mt-1 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                                   'placeholder': 'Ingresa tu nombre de usuario'}))
    
    email = forms.EmailField(label="Correo Electrónico",
                            widget=forms.EmailInput(attrs={
                                'class': 'w-full px-3 py-2 mt-1 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                                'placeholder': 'Ingresa tu email'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 mt-1 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Ingresa tu contraseña'
    }))

    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 mt-1 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Repite tu contraseña'
    }))
    alias = forms.CharField(label="Alias", max_length=30, 
                            widget=forms.TextInput(attrs={
                                'class': 'w-full px-3 py-2 mt-1 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                                'placeholder': 'Ingresa tu alias'}))
    
    avatar = forms.ImageField(label="Avatar", required=False, 
                              widget=forms.FileInput(attrs={   
                                  'class': 'mt-1 text-gray-400',}))
    
# Formulario para el login /autenticarse
class LoginForm (AuthenticationForm):
    username = forms.CharField( 
        max_length=254, label="Usuario",
        widget=forms.TextInput( 
            attrs={'class': 'form-control w-full px-3 py-2 mt-1 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                   'placeholder': 'Ingresa tu Usuario'}), 
    # Django form trabaja con widgets 
    # Los widgets son los elementos que se renderizan en el HTML 
    # Pueden recibir atributos como clases, id, placeholder, etc 
    ) 
    password = forms.CharField( label= "Contraseña",
        widget=forms.PasswordInput( attrs={'class': 'form-control w-full px-3 py-2 mt-1 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 
                                           'placeholder': 'Ingresa tu Contraseña'}), )