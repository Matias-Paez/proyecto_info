#from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here. aca se crean las views , las vistas

class UserProfileview (TemplateView):
    template_name = 'user/user_profile.html' #este es el templete / html que utiliza la vista (que se encuentre en templete/user)

