import json, jwt

from django.test    import TestCase, Client
from freezegun      import freeze_time

from users.models   import User, UserType
from .models        import Question, Comment, QuestionLike, QuestionType
from my_settings    import SECRET_KEY, ALGORITHM

client = Client()

class QuestionTest(TestCase):
    maxDiff = None
    def setUp(self):

        u_type1 = UserType.objects.create(
            id = 1,
            name = "user"
        )
        user1 = User.objects.create(
                id = 1,
                email = 'test1@test.com',
                password = 'pw12341234',
                name = 'tester1',
                user_type = u_type1
            )
        user2 = User.objects.create(
                id = 2,
                email = 'test2@test.com',
                password = 'pw12341234',
                name = 'tester2',
                user_type = u_type1
            )
        user3 = User.objects.create(
                id = 3,
                email = 'test3@test.com',
                password = 'pw12341234',
                name = 'tester3',
                user_type = u_type1
            )
        QuestionType.objects.create(
            id=1,
            name="기타"
        )
        q_type2 = QuestionType.objects.create(
            id=2,
            name="계정"
        )
        self.question1 = Question.objects.create(
                id = 1,
                writter = user1,
                title = 'test_q1_date',
                content = 'test_q1_content',
                created_at = '2021-03-03',
                updated_at = '2021-03-03'
        )
        self.question2 = Question.objects.create(
                id = 2,
                writter = user2,
                title = 'test_q2_weather',
                content = 'test_q2_content',
                created_at = '2021-04-03',
                updated_at = '2021-04-03'
        )
        self.question3 = Question.objects.create(
                id = 3,
                writter = user2,
                title = 'test_q3_place',
                content = 'test_q3_content',
                question_type = q_type2,
                created_at = '2021-04-03',
                updated_at = '2021-04-03'
        )

    def tearDown(self):
        User.objects.all().delete()
        Question.objects.all().delete()
        Comment.objects.all().delete()
        UserType.objects.all().delete()
        QuestionType.objects.all().delete()

    def test_question_post_success(self):
        """
        질문 등록 성공
        """
        data = {
            'writter' : 1,
            'title' : 'new_question',
            'content' : 'test'
        }
        user  = User.objects.get(id=1)
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/questions', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': '새 질문이 등록되었습니다', 'result' : data['title']})

    def test_question_post_fail_noinput_title(self):
        """
        Error : 필수 parameter 미입력 (제목)
        """
        data = {
            'writter' : 1,
            'content' : 'test'
        }
        user  = User.objects.get(id=1)
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/questions', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': '질문 제목을 입력해주세요'})
    
    def test_question_post_fail_noinput_content(self):
        """
        Error : 필수 parameter 미입력 (내용)
        """
        data = {
            'writter_id' : 1,
            'title' : 'new_question'
        }
        user  = User.objects.get(id=1)
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/questions', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': '질문 내용을 채워주세요'})

    def test_question_get_success(self):
        """
        성공 : 질문 목록 반환
        """
        response = client.get('/questions', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'question_list' : [{
                                                                        'title': 'test_q1_date',
                                                                        'content': 'test_q1_content',
                                                                        'created_at': self.question1.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                                                        'question_type': '기타',
                                                                        'writter': 'tester1',
                                                                        'like_num': 0
                                                                        }, {
                                                                        'title': 'test_q2_weather',
                                                                        'content': 'test_q2_content',
                                                                        'created_at': self.question2.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                                                        'question_type': '기타',
                                                                        'writter': 'tester2',
                                                                        'like_num': 0
                                                                        }, {
                                                                        'title': 'test_q3_place',
                                                                        'content': 'test_q3_content',
                                                                        'created_at': self.question3.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                                                        'question_type': '계정',
                                                                        'writter': 'tester2',
                                                                        'like_num': 0
                                                                        }]
                                                })

    def test_question_get_success_questiontypes_filtering(self):
        """
        성공 : 질문 유형으로 filtering (질문유형 : 기타)
        """
        response = client.get('/questions?type=1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'questions' : [{
                                                                        'content': 'test_q1_content',
                                                                        'created_at': self.question1.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                                                        'like_num': 0,
                                                                        'question_type': '기타',
                                                                        'title': 'test_q1_date',
                                                                        'writter': 'tester1'}]
                                            })

    def test_question_get_success_questiontypes_filtering(self):
        """
        성공 : 질문 유형으로 filtering (질문유형 : 계정)
        """
        response = client.get('/questions?type=2', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'question_list' : [{
                                                                            'title': 'test_q3_place',
                                                                            'content': 'test_q3_content',
                                                                            'created_at': self.question3.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                                                            'question_type': '계정',
                                                                            'writter': 'tester2',
                                                                            'like_num': 0
                                                                            }]
                                                })
    def test_question_get_success_keyword_search(self):
        """
        성공 : 질문과 본문에 있는 Keyword로 검색
        """
        response = client.get('/questions?keyword=date', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'question_list' : [{
                                                                        'title' : 'test_q1_date',
                                                                        'content': 'test_q1_content',
                                                                        'created_at': self.question1.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                                                        'question_type': '기타',
                                                                        'writter' : 'tester1',
                                                                        'like_num': 0,
                                                                        }]
                                            })
    def test_question_delete_success(self):
        """
        성공 : 질문 삭제 (DB에서의 삭제)
        """
        data = {
            'question_id' : [2, 3]
        }
        user  = User.objects.get(name='tester2')
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.delete('/questions', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 204)

    def test_question_delete_fail_invalid_user(self):
        """
        Error : 작성자가 아닌 유저의 접근
        """

        data = {
            'question_id' : [1]
        }
        user  = User.objects.get(name='tester2')
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.delete('/questions', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'message': '권한이 없습니다'})



class QuestionDetailTest(TestCase):
    def setUp(self):
        u_type1 = UserType.objects.create(
            id = 1,
            name = "user"
        )
        user1 = User.objects.create(
                id = 1,
                email = 'test1@test.com',
                password = 'pw12341234',
                name = 'tester1',
                user_type = u_type1
            )
        user2 = User.objects.create(
                id = 2,
                email = 'test2@test.com',
                password = 'pw12341234',
                name = 'tester2',
                user_type = u_type1
            )
        user3 = User.objects.create(
                id = 3,
                email = 'test3@test.com',
                password = 'pw12341234',
                name = 'tester3',
                user_type = u_type1
            )
        QuestionType.objects.create(
            id=1,
            name="기타"
        )
        q_type2 = QuestionType.objects.create(
            id=2,
            name="계정"
        )
        question1 = Question.objects.create(
                id = 1,
                writter = user1,
                title = 'test_q1_date',
                content = 'test_q1_content',
                created_at = '2021-04-03'
        )
        question2 = Question.objects.create(
                id = 2,
                writter = user2,
                title = 'test_q2_weather',
                content = 'test_q2_content',
                created_at = '2021-04-03'
        )
        question3 = Question.objects.create(
                id = 3,
                writter = user2,
                title = 'test_q3_place',
                content = 'test_q3_content',
                question_type = q_type2,
                created_at = '2021-04-03'
        )
        question4 = Question.objects.create(
                id = 4,
                writter = user2,
                title = 'test_q4',
                content = 'test_q4_content',
                is_delete = 1,
                created_at = '2021-04-03'
        )

    def tearDown(self):
        User.objects.all().delete()
        Question.objects.all().delete()
        UserType.objects.all().delete()
        QuestionType.objects.all().delete()

    def test_question_patch_success(self):
        """
        성공 : 질문 내역 수정 (일부 항목 수정 가능)
        """
        data = {
            'title' : 'test_q1_volunteer'
        }
        user  = User.objects.get(name='tester1')
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.patch('/questions/1', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': '수정이 완료되었습니다'})

    def test_question_patch_fail_invalid_user(self):
        """
        Error : 작성자가 아닌 유저의 접근
        """
        data = {
            'title' : 'test_q1_volunteer'
        }
        user  = User.objects.get(name='tester2')
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.patch('/questions/1', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'message': '권한이 없습니다'})

    def test_question_soft_delete_success(self):
        """
        성공 : 질문 내역 삭제 (soft_delete : is_delete의 값을 1로 변환 / DB에는 그대로 존재 / "숨김" 처리를 고려한 기능)
        """
        user = User.objects.get(name="tester1")
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.delete('/questions/1', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : '삭제처리 되었습니다'})

    def test_question_soft_delete_fail_already_deleted(self):
        """
        Error : 이미 soft_delete처리 되어있는 경우
        """
        user = User.objects.get(name="tester2")
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.delete('/questions/4', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : '이미 삭제된 질문입니다'})


class CommentTest(TestCase):
    def setUp(self):
        u_type1 = UserType.objects.create(
            id = 1,
            name = "user"
        )
        user1 = User.objects.create(
                id = 1,
                email = 'test1@test.com',
                password = 'pw12341234',
                name = 'tester1',
                user_type = u_type1
            )
        user2 = User.objects.create(
                id = 2,
                email = 'test2@test.com',
                password = 'pw12341234',
                name = 'tester2',
                user_type = u_type1
            )
        user3 = User.objects.create(
                id = 3,
                email = 'test3@test.com',
                password = 'pw12341234',
                name = 'tester3',
                user_type = u_type1
            )
        QuestionType.objects.create(
            id=1,
            name="기타"
        )
        q_type2 = QuestionType.objects.create(
            id=2,
            name="계정"
        )
        question1 = Question.objects.create(
                id = 1,
                writter = user1,
                title = 'test_q1_date',
                content = 'test_q1_content',
                created_at = '2021-04-03'
        )
        question2 = Question.objects.create(
                id = 2,
                writter = user2,
                title = 'test_q2_weather',
                content = 'test_q2_content'
        )
        question3 = Question.objects.create(
                id = 3,
                writter = user2,
                title = 'test_q3_place',
                content = 'test_q3_content',
                question_type = q_type2
        )
        self.q1_comment1 = Comment.objects.create(
                id = 1,
                writter = user2,
                question = question1,
                comment = 'test_q1_c1'
        )
        self.q1_comment1_recomment1 = Comment.objects.create(
                id = 2,
                writter = user1,
                question = question1,
                comment = 'thank you',
                is_parent_id = 1
        )
        q2_comment1 = Comment.objects.create(
                id = 3,
                writter = user2,
                question = question2,
                comment = 'test_q2_c1'
        )
        q2_comment2 = Comment.objects.create(
                id = 4,
                writter = user3,
                question = question2,
                comment = 'test_q2_c2'
        )
    def tearDown(self):
        User.objects.all().delete()
        UserType.objects.all().delete()
        Question.objects.all().delete()
        QuestionType.objects.all().delete()
        Comment.objects.all().delete()


    def test_comment_get_success(self):
        """
        성공 : 해당 질문의 답변 목록 반환
        """
        self.maxDiff = None
        response = client.get('/questions/1/comments', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'comment_list': [{
                                                                            'writter': 'tester2',
                                                                            'quetion_id': 1,
                                                                            'comment': 'test_q1_c1',
                                                                            'is_parent': None,
                                                                            'created_at': self.q1_comment1.created_at.strftime('%Y-%m-%d %H:%M:%S')
                                                                            }, {
                                                                            'writter': 'tester1',
                                                                            'quetion_id': 1,
                                                                            'comment': 'thank you',
                                                                            'is_parent': 1,
                                                                            'created_at': self.q1_comment1_recomment1.created_at.strftime('%Y-%m-%d %H:%M:%S')
                                                                            }]
                                            })
   
class QuestionLikeTest(TestCase):
    def setUp(self):       
        u_type1 = UserType.objects.create(
            id = 1,
            name = "user"
        )
        user1 = User.objects.create(
                id = 1,
                email = 'test1@test.com',
                password = 'pw12341234',
                name = 'tester1',
                user_type = u_type1
            )
        user2 = User.objects.create(
                id = 2,
                email = 'test2@test.com',
                password = 'pw12341234',
                name = 'tester2',
                user_type = u_type1
            )
        user3 = User.objects.create(
                id = 3,
                email = 'test3@test.com',
                password = 'pw12341234',
                name = 'tester3',
                user_type = u_type1
            )
        QuestionType.objects.create(
            id=1,
            name="기타"
        )
        q_type2 = QuestionType.objects.create(
            id=2,
            name="계정"
        )
        question1 = Question.objects.create(
                id = 1,
                writter = user1,
                title = 'test_q1_date',
                content = 'test_q1_content',
        )
        question2 = Question.objects.create(
                id = 2,
                writter = user2,
                title = 'test_q2_weather',
                content = 'test_q2_content'
        )
        question3 = Question.objects.create(
                id = 3,
                writter = user2,
                title = 'test_q3_place',
                content = 'test_q3_content',
                question_type = q_type2
        )
        QuestionLike.objects.create(
            user_id = 2,
            question_id = 1
        )
    def tearDown(self):
        User.objects.all().delete()
        UserType.objects.all().delete()
        Question.objects.all().delete()
        QuestionType.objects.all().delete()
        QuestionLike.objects.all().delete()

    def test_new_questionlikes_post_success(self):
        """
        성공 : 새로 질문에 대한 "좋아요" 등록
        """
        data = {
            "question_id" : 1
        }
        user  = User.objects.get(name='tester1')
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/questions/like', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': '좋아요가 등록되었습니다'})

    def test_delete_questionlikes_post_success(self):
        """
        성공 : 질문에 대한 "좋아요" 취소
        """
        data = {
            "question_id" : 1
        }
        user  = User.objects.get(name='tester2')
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/questions/like', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 200)

    def test_questionlikes_post_fail_doesnotexists(self):
        """
        Error : 유효하지 않은 질문에 대한 "좋아요" 기능 시
        """
        data = {
            "question_id" : 100
        }
        user  = User.objects.get(name='tester1')
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/questions/like', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': '존재하지 않는 질문입니다'})


class BestQuestionView(TestCase):
    def setUp(self):
        u_type1 = UserType.objects.create(
            id = 1,
            name = "user"
        )
        user1 = User.objects.create(
                id = 1,
                email = 'test1@test.com',
                password = 'pw12341234',
                name = 'tester1',
                user_type = u_type1
            )
        user2 = User.objects.create(
                id = 2,
                email = 'test2@test.com',
                password = 'pw12341234',
                name = 'tester2',
                user_type = u_type1
            )
        user3 = User.objects.create(
                id = 3,
                email = 'test3@test.com',
                password = 'pw12341234',
                name = 'tester3',
                user_type = u_type1
            )
        QuestionType.objects.create(
            id=1,
            name="기타"
        )
        q_type2 = QuestionType.objects.create(
            id=2,
            name="계정"
        )
        self.freezer = freeze_time("2021-03-20 00:00:00")
        self.freezer.start()
        question1 = Question.objects.create(
                id = 1,
                writter = user1,
                title = 'test_q1_date',
                content = 'test_q1_content'
        )
        self.freezer.stop()
        self.freezer = freeze_time("2021-04-20 00:00:00")
        self.freezer.start()
        question2 = Question.objects.create(
                id = 2,
                writter = user2,
                title = 'test_q2_weather',
                content = 'test_q2_content'
        )
        question3 = Question.objects.create(
                id = 3,
                writter = user2,
                title = 'test_q3_place',
                content = 'test_q3_content',
                question_type = q_type2
        )
        self.freezer.stop()

        QuestionLike.objects.create(
            user_id = 1,
            question_id = 2
        )
        QuestionLike.objects.create(
            user_id = 2,
            question_id = 3
        )
        QuestionLike.objects.create(
            user_id = 1,
            question_id = 3
        )
    def tearDown(self):
        User.objects.all().delete()
        UserType.objects.all().delete()
        Question.objects.all().delete()
        QuestionType.objects.all().delete()
        QuestionLike.objects.all().delete()

    def test_bestquestion_get_success(self):
        """
        성공 : 기준 월의 가장 좋아요 많은 질문 반환
        """
        self.maxDiff = None
        response = client.get('/questions/best/2', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'best_question' : {
                                                                        'writter': 'tester2',
                                                                        'question_type': '계정', 
                                                                        'title': 'test_q3_place',
                                                                        'content': 'test_q3_content',
                                                                        'created_at': '2021-04-20'
                                                                        }
                                            })

    def test_bestquestion_get_success_nodata(self):
        """
        성공 : 기준 월의 질문목록들 중 좋아요 받은것이 하나도 없을 경우
        """
        response = client.get('/questions/best/1', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : '해당되는 조건이 없습니다'})