from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList 
from apps.post.models import Post, PostImage 


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

"""
#dejo esto si no anda
class UpdatePostForm(PostForm): 
    image = forms.ImageField(required = False)
    
    def __init__(self, *args, **kwargs): # Obtenemos las imagenes activas del form
         self.active_images =  kwargs.pop('active_images' , None)
         super(UpdatePostForm, self).__init__(*args, **kwargs)

         if self.active_images:
              for image in self.active_images:
                   field_name = f"keep_image_{image.id}"
                   self.fields[field_name]= forms.BooleanField( required= False, initial= True , label= f"Mantener {image}")
    
    def save(self, commit=True): 
        post = super().save(commit=False) 
        
        if commit: 
            post.save() 
            if self.cleaned_data['image']:  # Si el usuario sube una nueva imagen 
                PostImage.objects.create(post=post, image=self.cleaned_data['image']) 

            if self.active_images:  # Si hay imágenes activas y se quiere mantener alguna 
                for image in self.active_images: 
                    if not self.cleaned_data.get(f"keep_image_{image.id}", True): 
                        image.delete() # Eliminar la imagen si el usuario no la quiere mantener, checkboxes desmarcados 
        return post 
"""