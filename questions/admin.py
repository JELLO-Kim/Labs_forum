from django.contrib import admin

# Register your models here.

from questions.models import Question, Comment, QuestionLike, QuestionType

class QuestionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment, QuestionAdmin)
admin.site.register(QuestionLike, QuestionAdmin)
admin.site.register(QuestionType, QuestionAdmin)