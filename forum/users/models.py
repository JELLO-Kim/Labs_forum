from django.db import models

class User(models.Model):
    email       = models.CharField(max_length=50, unique=True)
    password    = models.CharField(max_length=300)
    name        = models.CharField(max_length=30, unique=True, null=True)
    user_type   = models.ForeignKey('UserType', on_delete=models.CASCADE)
    last_login  = models.DateTimeField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    deleted_at  = models.DateTimeField(null=True)
    is_delete   = models.BooleanField(default=0)

    class Meta:
        db_table = 'users'

class UserType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'user_types'