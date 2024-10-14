#from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here. aca se crean las views , las vistas

class PostDetailView (TemplateView):
    template_name = 'post/post_detail.html'


class PostUpdateView (TemplateView):
    template_name = 'post/post_update.html'