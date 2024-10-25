from django.db import models
from django.contrib.auth.models import AbstractUser # me va permitir 

import os
import uuid
# Create your models here.


def get_avatar_filename(instance , filename):
    base_filename , file_extension = os.path.splitext(filename)  #para separar nombre-extencion
    new_filename = f"user_{instance.id}_avatar{file_extension}"
    return os.path.join('user/avatar/', new_filename)


class User(AbstractUser):
    #defino los atributos campos que guardo en la DB
    id = models.UUIDField(primary_key = True ,default= uuid.uuid4, editable= False) # defino mi tipo de id en este caso un tipo bb21iijsksdi12
    alias = models.CharField(max_length = 35 , blank = True)
    avatar = models.ImageField(upload_to = get_avatar_filename , default= 'user/default/avatar_default.png' )

    #Collaborator- devuelve un booleano
    @property
    def is_collaborator(self):
        return self.groups.filter(name = 'Collaborators').exists()
    
    #Registereds 
    @property
    def is_registered(self):
        return self.groups.filter(name = 'Registereds').exists()
    
    #Administrators
    @property
    def is_administrator(self):
        return self.groups.filter(name = 'Administrators').exists()
    




