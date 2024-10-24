#from django.shortcuts import render
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView , CreateView, DetailView , DeleteView , UpdateView
from django.urls import reverse , reverse_lazy
from django.conf import settings

from apps.post.models import Post , PostImage, Category # importo el modelo y el form
from apps.post.forms import NewPostForm, UpdatePostForm
# Create your views here. aca se crean las views , las vistas

#Vista para ver el post
class PostDetailView (DetailView):
    template_name = 'post/post_detail.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        #Obtener todas las imágenes activas del post 
        active_images = self.object.images.filter(active=True) # Solo las que estan en True
        context['active_images'] = active_images 
        return context 

#Vista para actualizar el post
class PostUpdateView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = 'post/post_update.html'

    def get_context_data(self, **kwargs):
        # Agregamos las imágenes activas al contexto para ser manejadas en la plantilla
        context = super().get_context_data(**kwargs)
        context['active_images'] = self.get_object().images.filter(active=True)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        active_images = self.get_object().images.filter(active=True)
        keep_any_image_active = False

        # Manejo de imágenes activas
        for image in active_images:
            field_name = f"keep_image_{image.id}"
            if not form.cleaned_data.get(field_name, True): # Eliminar si no esta seleccionado el check
                image.active = False 
                image.save()
            else:
                keep_any_image_active = True
            
        # Manejo de nuevas imágenes subidas
        new_images = self.request.FILES.getlist('images')
        if new_images:
            for image in new_images:
                PostImage.objects.create(post=post, image=image)

        # Si no se desea mantener ninguna imagen activa y no se subieron nuevas imágenes
        if not keep_any_image_active and not new_images:
            PostImage.objects.create(post=post, image=settings.DEFAULT_POST_IMAGE)

        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.slug})

#Para Manejar el Listado de posteos
class PostListView(ListView):
    model = Post
    template_name= 'post/post_list.html'
    context_object_name = 'posts' # nombre del contexto

    def get_queryset(self):
        queryset = Post.objects.all()

        # Filtros
        title = self.request.GET.get('title', '')
        category_id = self.request.GET.get('category', '')

        if title:
            queryset = queryset.filter(title__icontains=title)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Pasa las categorías al contexto

        return context 

#Vista para eliminar Post
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post:post_list')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

#vista para crear el fomulario
class PostCreateView(CreateView):
    template_name = 'post/post_create.html'
    form_class = NewPostForm
    model = Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        
        #obtengo las imagnees cargadas por el usuario
        images = self.request.FILES.getlist('images')

        #si subio , las asocio al post
        if images:
            for image in images:
                PostImage.objects.create(post=post, image= image)
        else:
            PostImage.objects.create(post=post, image=settings.DEFAULT_POST_IMAGE)

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Pasa las categorías al contexto

        return context 
    
    def get_success_url(self):
        return reverse('post:post_detail', kwargs= {'slug': self.object.slug}) #Me dirijo al posteo mediante el slug

