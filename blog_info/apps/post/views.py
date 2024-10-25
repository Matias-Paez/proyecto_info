#from django.shortcuts import render
from django.forms import BaseModelForm
from django.http import HttpResponse , HttpResponseForbidden
from django.views.generic import ListView , CreateView, DetailView , DeleteView , UpdateView , View
from django.urls import reverse , reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404 , redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 

from apps.post.models import Post , PostImage, Category , Comment# importo el modelo y el form
from apps.post.forms import NewPostForm, UpdatePostForm , NewCategoryForm, UpdateCategoryForm , CommentForm

#Vistas para comentarios
#Nuevo comentarios
class CommentCreateView(CreateView): 
    model = Comment 
    form_class = CommentForm 
    template_name = 'post/post_detail.html' 
    
    def form_valid(self, form):
        form.instance.author = self.request.user 
        form.instance.post = Post.objects.get(slug=self.kwargs['slug']) 

        return super().form_valid(form) 
    
    def get_success_url(self): 
        return reverse_lazy('post:post_detail', kwargs={'slug':self.object.post.slug}) 
#Editar un comentario
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Comment 
    fields = ['content']
    template_name = 'comment/comment_update.html' 

    def test_func(self):
        # Solo el autor puede actualizar el comentario
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self): 
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.post.slug}) 
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
     
# Eliminar un comentario
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_superuser

    def get_object(self):
        comment_id = self.kwargs.get('pk')
        return get_object_or_404(Comment, id=comment_id)

    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return redirect('post:post_detail', slug=comment.post.slug)  # Redirige al post después de eliminar


#Vista para ver el post
class PostDetailView(DetailView):
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


#VISTAS PARA CATEGORIAS
#Vista Para ver categorias
class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name ='categories'
    

#Vista para crear categoria 
class CategoryCreateView(CreateView):
    model= Category
    template_name= 'category/category_create.html'
    form_class = NewCategoryForm
    success_url = reverse_lazy('post:category_list')

    def form_valid(self, form):
        messages.success(self.request, "La categoría ha sido creada con éxito.")
        return super().form_valid(form)

#Vista para Actualizar categoria
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = UpdateCategoryForm
    template_name = 'category/category_update.html'
    success_url = reverse_lazy('post:category_list')  # URL a la que redirigir después de una actualización

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Categoría'
        return context
    
    def form_valid(self , form):
        messages.success(self.request, "La categoría ha sido actualizada con éxito.")
        return super().form_valid(form)


    
#Vista para eliminar Categoria-- se hace desde categori_detail- sin un form - lo mismo que post delete
class CategoryDeleteView(DeleteView):
    model = Category     
    success_message = "La categoría ha sido eliminada con éxito."
    success_url = reverse_lazy('post:category_list')  # URL a la que redirigir después de una actualización

    def delete(self, request, *args, **kwargs):
        # Establecer el mensaje
        messages.success(request, "La categoría ha sido eliminada con éxito.")
        # Usar la llamada al super() con return directamente
        return super().delete(request, *args, **kwargs)
    