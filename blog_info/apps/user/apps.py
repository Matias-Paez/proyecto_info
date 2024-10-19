from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user' #debo poner eso aca para que lo encuentre

    def ready(self) :
        import apps.user.signals


# def ready(self) -> None:
#return super().ready()