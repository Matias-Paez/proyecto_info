# Son las señales que nos manda django
# Creo los grupos y permisos
# **kwars vienen por parametro
from django.db.models.signals import post_save 
from django.contrib.auth.models import Permission , Group
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from apps.user.models import User
from apps.post.models import Post , Comment , Category


@receiver(post_save, sender = User) # esto es un decorador
def create_groups_permissions(sender , instance, created , **kwargs):
    
    if created and instance.is_superuser : #si la instancia es de super user
        try:
            post_content_type = ContentType.objects.get_for_model(Post)
            comment_content_type = ContentType.objects.get_for_model(Comment)
            category_content_type = ContentType.objects.get_for_model(Category)

            # Permisos de Post
            view_post_permission= Permission.objects.get( codename = 'view_post', content_type = post_content_type)
            add_post_permission= Permission.objects.get( codename = 'add_post', content_type = post_content_type)
            change_post_permission= Permission.objects.get( codename = 'change_post', content_type = post_content_type)
            delete_post_permission= Permission.objects.get( codename = 'delete_post', content_type = post_content_type)

            # Permisos de comentarios
            view_comment_permission= Permission.objects.get( codename = 'view_comment', content_type = comment_content_type)
            add_comment_permission= Permission.objects.get( codename = 'add_comment', content_type = comment_content_type)
            change_comment_permission= Permission.objects.get( codename = 'change_comment', content_type = comment_content_type)
            delete_comment_permission= Permission.objects.get( codename = 'delete_comment', content_type = comment_content_type)

            # Permisos de Categorias - solo para visualizar
            view_category_permission= Permission.objects.get( codename = 'view_category', content_type = category_content_type)

            registered_group , created = Group.objects.get_or_create(name = 'Registereds') 
            # Le doy estos permisos a los registrados
            registered_group.permissions.add(
                view_comment_permission,
                add_comment_permission,
                change_comment_permission,
                delete_comment_permission
                )
            # Le doy permisos a los colaboradores
            collaborator_group , created = Group.objects.get_or_create(name = 'Collaborators') 

            collaborator_group.permissions.add(
                #permisos de comentarios
                view_comment_permission,
                add_comment_permission,
                change_comment_permission,
                delete_comment_permission,
                #permisos de post
                view_post_permission,
                add_post_permission,
                change_post_permission,
                delete_post_permission,
                #permisos de category - para que las vean
                view_category_permission
                )
            
            # Le doy permisos a los admins -- TODOS
            administrator_group , created = Group.objects.get_or_create(name = 'Administrators') 

            administrator_group.permissions.set(Permission.objects.all())

        except ContentType.DoesNotExist :
            print('El tipo de contenido aún no exite')
        
        except Permission.DoesNotExist:
            print('Algunos permisos no estan distonibles')
    
