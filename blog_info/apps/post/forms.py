from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList 
from apps.post.models import Post, PostImage , Category


class PostForm(forms.ModelForm): 
    class Meta: 
            model = Post 
            fields = ('title', 'content','category' , 'allow_comment')

#Formulario para un nuevo posteo
class NewPostForm(PostForm):
    image = forms.ImageField(required=False) 
    
    def save(self, commit=True): 
        post = super().save(commit=False) 
        image = self.cleaned_data['image'] 

        if commit:
            post.save() 
            if image:
                PostImage.objects.create(post=post, image=image) 
        return post 

#Formulario para actualizar posteo
class UpdatePostForm(PostForm):
    images = forms.ImageField(required = False)
    
    def __init__(self, *args, **kwargs): 
        super(UpdatePostForm, self).__init__(*args, **kwargs)
        # No necesitamos 'active_images' aquí, ya que las manejarás en la vista/plantilla

    def save(self, commit=True): 
        post = super().save(commit=False)

        if commit:
            post.save()

            # Subida de nuevas imágenes
            new_images = self.files.getlist('images')
            if new_images:
                for image in new_images:
                    PostImage.objects.create(post=post, image=image)

        return post

#Formulario Para las Categorias
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title' , 'description')
        

#Nueva Categoria
class NewCategoryForm(CategoryForm):
    pass

#Actualizar categoria

class UpdateCategoryForm(CategoryForm):
    pass