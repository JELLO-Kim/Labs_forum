import json

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Count, Q

from users.models       import User
from questions.models   import Question, Comment, QuestionLike, QuestionType
from utils              import login_decorator

class QuestionView(View):
    def get(self, request):
        """
        Author:
            - Chae hyun Kim
        Args:
            - Case Search : keyword
            - Case Filtering : type
        Return:
            - 200: {'message' : 'SUCCESS', 'result' : question_list}
        Note:
            - is_delete값이 0인 question만 반환
        """
        keyword = request.GET.get('keyword', None)
        type = request.GET.get('type', None)

        questions = Question.objects.select_related('writter', 'question_type').prefetch_related('questionlike_set').filter(is_delete=0)

        if keyword:
            questions = questions.filter(
				Q(title__icontains=keyword) | Q(content__icontains=keyword)
            )
        if type:
            if not QuestionType.objects.filter(id=type).exists():
                return JsonResponse({'message' : '유효하지 않은 질문 타입입니다.'}, status=400)
            questions = questions.filter(question_type_id=type)

        question_list = [{
            'title' : question.title,
            'content' : question.content,
            'created_at' : question.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'question_type' : question.question_type.name,
            'writter' : question.writter.name,
            "like_num" : question.user_like.count()
        } for question in questions]
        return JsonResponse({'message' : 'SUCCESS', 'question_list' : question_list}, status=200)

    @login_decorator
    def post(self, request):
        """
        Author:
            - Chae hyun Kim
        Args:
            - title
            - content
            - optional) question_type : 없을경우 1(기타) 유형으로 등록된다.
        Return:
            - 200: {'message' : '새 질문이 등록되었습니다', 'result' : question.title}
            - 400: '질문 제목을 입력해주세요'
            - 400: '질문 내용을 채워주세요'
        """
        user = request.user
        data = json.loads(request.body)
        title = data.get('title', None)
        content = data.get('content', None)
        question_type = data.get('question_type', None)

        # Key Validation
        if not title:
            return JsonResponse({'message': '질문 제목을 입력해주세요'}, status=400)
        if not content:
            return JsonResponse({'message': '질문 내용을 채워주세요'}, status=400)
       
        question = Question.objects.create(
                    writter = user,
                    title = title,
                    content = content
                )
        
        if question_type:
            question.question_type = question_type
            question.save()

        return JsonResponse({'message' : '새 질문이 등록되었습니다', 'result' : question.title}, status=201)

    @login_decorator
    def delete(self, request):
        """
        Author:
            - Chae hyun Kim
        Args:
            - question_id (list형태) : body로 받는다
        Return:
            -204: hard_Delete
            -403: (작성자가 아닌 유저가 접근했을때) 권한이 없습니다
        """
        user = request.user
        data = json.loads(request.body)
        delete_list = data['question_id']

        for row in delete_list:
            if Question.objects.get(id=row).writter != user:
                return JsonResponse({'message' : '권한이 없습니다'}, status=403)
            else:
                Question.objects.get(id=row).delete()
        return JsonResponse({'message' : 'DELETE'}, status=204)

class QuestionDetailView(View):
    @login_decorator
    def patch(self, request, question_id):
        """
        Authors:
            - Chae hyun Kim
        Args:
            - optional) 바꿀 목록 (title, content, question_type)
        Return:
            - 200: {'message': '수정이 완료되었습니다.'}
        Note:
            - quetion_type은 해당 값의 id값으로 받는다.
                예) "기타(id=1)"에서 "계정(id=2)"로 변경시 2 의 값을 받는다.        
        """
        user = request.user
        data = json.loads(request.body)
        title = data.get('title', None)
        content = data.get('content', None)
        question_type = data.get('question_type_id', None)

        question = Question.objects.get(id=question_id)

        # 유효하지 않은 질문번호 Validation
        if Question.objects.get(id=question_id).is_delete == 1:
            return JsonResponse({'message' : '이미 삭제된 질문입니다.'})
        if not Question.objects.filter(id=question_id).exists():
            return JsonResponse({'message' : '존재하지 않는 질문입니다'}, status=404)

        # 유효한 유저 Validation
        if Question.objects.get(id=question_id).writter != user:
            return JsonResponse({'message' : '권한이 없습니다'}, status=403)
        
        if title:
            question.title = title
        if content:
            question.content = content
        if question_type:
            question.question_type_id = question_type
        question.save()

        return JsonResponse({'message' : '수정이 완료되었습니다'}, status=200)
    @login_decorator
    def delete(self, request, question_id):
        """
        Author:
            - Chae hyun Kim
        Args:
            - 지울 question의 id : path parameter로 받는다
        Return:
            - 204
        Note:
            - delete method이지만 마치 "숨김" 기능처럼 soft_delete방식으로 질문을 처리한다 (is_delete의 값을 0에서 1로 변환)
        """
        user = request.user
        # 유효하지 않은 질문번호 Validation
        if Question.objects.get(id=question_id).is_delete:
            return JsonResponse({'message' : '이미 삭제된 질문입니다'}, status=400)
        if not Question.objects.filter(id=question_id).exists():
            return JsonResponse({'message' : '존재하지 않는 질문입니다'}, status=404)

        if Question.objects.get(id=question_id).writter != user:
            return JsonResponse({'message' : '권한이 없습니다'}, status=403)

        question = Question.objects.get(id=question_id)
        question.is_delete = 1
        question.save()

        return JsonResponse({'message' : '삭제처리 되었습니다'}, status=200)

class CommentView(View):
    @login_decorator
    def post(self, request, question_id):
        """
        Author:
            - Chae hyun Kim
        Args:
            - question_id : path parameter로 받는 값
            - comment
            - is_parent : 없어도 에러반환하진 않는다.
        Return:
            - 200: {'message' : 'SUCCESS', 'comment_list' : comment_list}
            - 400: 내용을 입력해 주세요
        """
        user = request.user
        data = json.loads(request.body)
        comment = data.get('comment', None)
        is_parent = data.get('is_parent', None)

        # 질문 유효성 Validation
        if Question.objects.get(id=question_id).is_delete == 1:
            return JsonResponse({'message' : '삭제된 질문입니다'}, status=400)

        # Key Validation
        if not comment:
            return JsonResponse({'message' : '내용을 입력해 주세요'})

        new_comment = Comment.objects.create(
                        writter = user,
                        question_id = question_id,
                        comment = comment
                    )
        if is_parent:
            new_comment.is_parent_id = is_parent
            new_comment.save()
        
        return JsonResponse({'message' : '댓글이 등록되었습니다'}, status=201)

    def get(self, request, question_id):
        if not Question.objects.filter(id=question_id).exists():
            return JsonResponse({'message' : '존재하지 않는 질문입니다'}, status=404)
        if Question.objects.get(id=question_id).is_delete == 1:
            return JsonResponse({'message' : '삭제된 질문입니다'}, status=400)
        comments = Comment.objects.filter(is_delete = 0, question_id=question_id)

        comment_list = [{
            'writter' : comment.writter.name,
            'quetion_id' : comment.question_id,
            'comment' : comment.comment,
            'is_parent' : comment.is_parent_id,
            'created_at' : comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for comment in comments]
        return JsonResponse({'message' : 'SUCCESS', 'comment_list' : comment_list}, status=200)

class QuestionLikeView(View):
    @login_decorator
    def post(self, request):
        """
        Author:
            - Chae hyun Kim
        Args:
            - question_id : body로 받는 값
        Return:
            -200: {'message' : '좋아요가 쥐소되었습니다'}
            -201: {'message' : '좋아요가 등록되었습니다'}}
        Note:
            - status_code 가 204인 경우 response의 body에 메세지가 담기지 않아 좋아요 취소시엔 200으로 지정.
        """
        user = request.user
        data = json.loads(request.body)
        question_id = data.get('question_id', None)
        if not Question.objects.filter(id=question_id).exists():
            return JsonResponse({'message' : '존재하지 않는 질문입니다'}, status=404)
        if Question.objects.get(id=question_id).is_delete == 1:
            return JsonResponse({'message' : '삭제된 질문입니다'}, status=400)
        if QuestionLike.objects.filter(user=user, question_id=question_id).exists():
            QuestionLike.objects.get(user=user, question_id=question_id).delete()
            return JsonResponse({'message' : '좋아요가 쥐소되었습니다'}, status=200)
        else:
            QuestionLike.objects.create(user=user, question_id=question_id)
            return JsonResponse({'message' : '좋아요가 등록되었습니다'}, status=201)

class BestQuestionView(View):
    def get(self, request, question_id):
        """
        Author:
            - Chae hyun Kim
        Args:
            - question_id: body로 받는 값
        Return:
            - 200: {'message' : 'SUCCESS', 'best_question' : best_question}
            - 200: {'message' : '해당되는 조건이 없습니다'}
        """

        if not Question.objects.filter(id=question_id).exists():
            return JsonResponse({'message' : '존재하지 않는 질문입니다'}, status=404)
        if Question.objects.get(id=question_id).is_delete == 1:
            return JsonResponse({'message' : '삭제된 질문입니다'}, status=400)

        check_question = Question.objects.get(id=question_id)
        standard_month = check_question.created_at.month
        questions = Question.objects.filter(created_at__month = standard_month).select_related('writter', 'question_type')
        best_question_select = questions.annotate(like_num=Count('questionlike')).order_by('-like_num')[0]

        # 해당 월의 질문들 중 좋아요 표시된 것이 하나도 없을 경우 : error는 아닌걸로 간주
        if best_question_select.like_num == 0:
            return JsonResponse({'message' : '해당되는 조건이 없습니다'}, status=200)

        best_question = {
            'writter' : best_question_select.writter.name,
            'question_type' : best_question_select.question_type.name,
            'title' : best_question_select.title,
            'content' : best_question_select.content,
            'created_at' : best_question_select.created_at.strftime('%Y-%m-%d')
        }

        return JsonResponse({'message' : 'SUCCESS', 'best_question' : best_question}, status=200)