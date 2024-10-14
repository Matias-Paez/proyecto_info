from django.views.generic import TemplateView #me permite importar/mostrar un template?

class IndexView(TemplateView):
    template_name = 'index.html'
    

