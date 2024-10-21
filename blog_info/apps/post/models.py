from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

import uuid
import os

# Create your models here. 
#Modelo de Categoria 
class Category (models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable=False)
    title = models.CharField(max_length= 60)
    description = models.TextField(max_length=120)

#Modelo de Post
class Post (models.Model):
    #defino los campos de mis post
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable= False)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique= True, max_length = 130) # el slug para que me lleve a un post e particular
    content = models.TextField(max_length=5000) # maximo tamaño del texto
    #relacion con el autor/colaborador
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE) #CASCADE Elimina todos los post asociados al usuario
    creation_date = models.DateTimeField (default= timezone.now ) # capturo el timpo en que se creo
    modification_date = models.DateTimeField(auto_now= True) # actializo a la ultima fecha de modificación
    allow_comment = models.BooleanField(default=True) # defino si se permite comentarios
    #relacion con categoria
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # aca defino la relacion con la categoria y la relacion con comentarios - Definir luego
    
    #metodos/funciones
    def __str__(self): 
        return self.title
    
    @property
    def amount_comments(self):
        #retorno la cantidad de comentarios del post
        return self.comments.count() 
    
    @property
    def amount_images (self):
        return self.images.count() # retorno la cantidad de imagenes asociadas que tiene el post
    
    #sobre escribo el metodo save que heredo de los modelos
    def save(self , *args, **kwargs):
        if not self.slug: # verifico que la instancia no tenga un slug generado ya
            self.slug = self.generate_unique_slug()
        #llamo al metodo super y guardo
        super().save(*args, **kwargs)
        ## esta parte no se si queda -- ver luego ##
        ''' ver luego esta parte TODO:'''
        if not self.images.exists():
            PostImage.objects.create(post.self, image = 'post/default/post_default.png')

    def generate_unique_slug(self):
        slug = slugify(self.title) #le pasamos lo que tiene que hacer
        unique_slug = slug
        num = 1
        #verifico que sea unico
        while Post.objects.filter(slug= unique_slug).exists(): # si existe coincidencias con los slug va a agregarle un numero
            unique_slug = f"{slug}-{num}"
            num += 1

        return unique_slug


# funcion para generar como los nombres de las imagenes con el id del post
def get_image_filename(instance, filename): 
    post_id = instance.post.id 
    images_count = instance.post.images.count() 
    base_filename, file_extension = os.path.splitext(filename) # esto se llama unpacking (desempaquetado) 
    new_filename = f"post_{post_id}_cover_{images_count + 1}{file_extension}" 
    return os.path.join('post/cover/', new_filename) 

#Modelo de imagen - relacion de 1 a n con post (un post tiene 1 o muchas imagnes)
class PostImage(models.Model): 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images') 
    image = models.ImageField(upload_to=get_image_filename, default='post/default/post_default.png') 
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self): 
        return f"PostImage {self.id}"

#Modelo de Comentarios
class Comment (models.Model):
    #defino los atributos/campos de la entidad 
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable=False)
    content = models.TextField(max_length= 300)
    creation_date = models.DateTimeField(auto_now_add= True) # cada vez que modifico se actualiza
    #Foreinkey con el author
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete= models.CASCADE) # si elimino el usuario elimino todos sus comentarios
    #ForeinKey con el post
    post = models.ForeignKey (Post , on_delete= models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content  # cuando llamo se muestra su contenido 
