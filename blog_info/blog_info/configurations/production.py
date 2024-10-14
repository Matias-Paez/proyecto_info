#todo esto es para deployar luego 
from .base import*

DEBUG = False

# TODO: Dejar aqui solo el dominio de produccion
ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        
        # en caso de querer conectarme a posgreSQL#
        #'ENGINE': 'django.db.backends.posgresql',
        
        # En caso de usar msqyl - todo esto debe configurarse - van a estar en el .env
        #'ENGINE':'django.db.backends.mysql',
        #NAME = os.getenv.('DB_NAME')
        #USER = os.getenv.('DB_USER')
        #PASSWORD: = os.getenv.('DB_PASSWORD')
        #HOST : os.getenv(DB_HOST)
        #PORT : os.getenv(DB_PORT)
    }
}

os.environ['DJANGO_PORT'] = '8080'