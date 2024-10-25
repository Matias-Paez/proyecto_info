from django.views.generic import TemplateView
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