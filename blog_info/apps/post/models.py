from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

import uuid


# Create your models here. 
#aqui voy a definir las categorias y los comentarios

class Post (models.Model):
    #defino los campos de mis post
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable= False)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique= True, max_length = 130) # el slug para que me lleve a un post e particular
    content = models.TextField(max_length=5000) # maximo tamaño del texto
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE) #CASCADE Elimina todos los post asociados al usuario
    creation_date = models.DateTimeField (default= timezone.now ) # capturo el timpo en que se creo
    modification_date = models.DateTimeField(auto_now= True) # actializo a la ultima fecha de modificación
    allow_comment = models.BooleanField(default=True) # defino si se permite comentarios
    ################################################################################
    category = models.ForeignKey ()  # aca defino la relacion con la categoria y la relacion con comentarios - Definir luego

    #metodos/funciones
    def __str__(self): 
        return self.title
    
    @property
    def amount_comments(self):
        #retorno la cantidad de comentarios del post
        return self.comments.count() 

    #sobre escribo el metodo save que heredo de los modelos
    def save(self , *args, **kwargs):
        if not self.slug: # verifico que la instancia no tenga un slug generado ya
            self.slug = self.generate_unique_slug()
        #llamo al metodo super y guardo
        super().save(*args, **kwargs)
        #TODO : como manejo las imagenes de portada?


    def generate_unique_slug(self):
        slug = slugify(self.title) #le pasamos lo que tiene que hacer
        #verifico que sea unico
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug= unique_slug).exists(): # si existe coincidencias con los slug va a agregarle un numero
            unique_slug = f"{slug}-{num}"
            num += 1

        return unique_slug



class Comment (models.Model):
    #defino los atributos/campos de la entidad 
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable=False)
    content = models.TextField(max_length= 300)
    creation_date = models.DateTimeField(auto_now_add= True) # cada vez que modifico se actualiza
    #Foreinkey con el author
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete= models.CASCADE) # si elimino el usuario elimino todos sus comentarios
    #ForeinKey con el post
    post = models.ForeignKey ( Post , on_delete= models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content  # cuando llamo se muestra su contenido 



#VER LUEGO los foreinjey en categorias

class Category (models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable=False)
    name = models.CharField(max_length= 80)
    description = models.TextField(max_length=200)

    #CRUD
