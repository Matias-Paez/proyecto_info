from django.views.generic import TemplateView
from django.shortcuts import render 
from apps.post.models import Post # importo el modelo de post


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtenemos todos los posts, ordenados por fecha de creación y solo envio los tres primeros
        context['posts'] = Post.objects.all().order_by('-creation_date')[:3]
        return context


class ContactView(TemplateView):
    template_name = 'contact.html'

# Es importante que el argumento exception esté presente
# para que Django lo pueda identificar como un manejador de errores

def error_403(request, exception=None):
    return render(request, 'errors/error_forbidden.html', status=403)

def error_404(request, exception=None):
    return render(request, 'errors/error_not_found.html', status=404)

def error_500(request):
    return render(request, 'errors/error_internal.html', status=500)