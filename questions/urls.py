from django.urls import path

from questions.views import QuestionView, QuestionDetailView, CommentView, QuestionLikeView, BestQuestionView

urlpatterns = [
    path('', QuestionView.as_view()),
    path('/<int:question_id>', QuestionDetailView.as_view()),
    path('/<int:question_id>/comments', CommentView.as_view()),
    path('/like', QuestionLikeView.as_view()),
    path('/best/<int:question_id>', BestQuestionView.as_view())
]