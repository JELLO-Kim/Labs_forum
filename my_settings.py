DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'labs_forum',
        'USER' : 'root',
        'PASSWORD' : 'Toohard',
        'HOST' : '127.0.0.1',
        'PORT' : '3306'
    }
}


# RDS ver.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'labs_forum',
#         'USER' : 'root',
#         'PASSWORD' : 'Toodifficult',
#         'HOST' : 'wecode-project.cpdsvq2c3ek9.ap-northeast-2.rds.amazonaws.com',
#         'PORT' : '3306'
#     }
# }

SECRET_KEY = 'django-insecure-go1bp935l#f!oawaycfe!!&p9grw^_pv=hu^u3rtsfcq@co136'

ALGORITHM = 'HS256'
