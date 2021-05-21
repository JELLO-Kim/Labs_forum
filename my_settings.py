DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'forum',
        'USER' : 'root',
        'PASSWORD' : 'password',
        'HOST' : 'db',
        'PORT' : '3306'
    }
}

SECRET_KEY = 'SECRET_KEY'

ALGORITHM = 'HS256'