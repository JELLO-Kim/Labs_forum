from django.db import models

from users.models import User

class QuestionType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'question_types'

class Question(models.Model):
    writter         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    question_type   = models.ForeignKey('QuestionType', on_delete=models.CASCADE, default=1)
    title           = models.CharField(max_length=150)
    content         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    deleted_at      = models.DateTimeField(null=True)
    is_delete       = models.BooleanField(default=0)

    class Meta:
        db_table = 'questions'

class Comment(models.Model):
    writter     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    question    = models.ForeignKey('Question', on_delete=models.CASCADE)
    comment     = models.TextField()
    is_parent   = models.ForeignKey('Comment', related_name='origin_comment', null=True, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    deleted_at  = models.DateTimeField(null=True)
    is_delete   = models.BooleanField(default=0)

    class Meta:
        db_table = 'comments'

class QuestionLike(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    class Meta:
        db_table = 'question_likes'