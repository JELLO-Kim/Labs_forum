import json, jwt

from django.test import TestCase, Client

from users.models   import User, UserType
from my_settings    import SECRET_KEY, ALGORITHM

client = Client()

class SignUpTest(TestCase):
    def setUp(self):
        UserType.objects.create(
            id = 1,
            name = "user"
        )

        user = User.objects.create(
                email = 'test1@test.com',
                password = 'pw12341234',
                name = 'tester1',
                user_type_id = 1
            )
    def tearDown(self):
        User.objects.filter(name='tester1').delete()

    def test_signup_post_success(self):
        data = {
            'email' : 'test5@test.com',
            'password' : 'pw12341234',
            'name' : 'tester5'
        }
        
        response = client.post('/user/signup', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': '회원가입 성공', 'result' : 'test5@test.com'})

    def test_signup_post_fail_duplicated_email(self):
        data = {
            'email' : 'test1@test.com',
            'password' : 'pw12341234',
            'name' : 'tester5'
        }
        response = client.post('/user/signup', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': '이미 사용중인 이메일입니다'})
        
    def test_signup_post_fail_short_password(self):
        data = {
            'email' : 'test5@test.com',
            'password' : 'pw',
            'name' : 'tester5'
        }
        response = client.post('/user/signup', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': '비밀번호는 8자 이상 입력해주세요'})

    # def test_signup_post_fail_invalid_password(self):
    #     data = {
    #         'email' : 'test5@test.com',
    #         'password' : '########',
    #         'name' : 'tester5'
    #     }
    #     response = client.post('/user/signup', json.dumps(data), content_type='application/json')
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json(), {'message': '특수문자는 @ ! ^ * 만 가능합니다'})

class SignInTest(TestCase):
    def setUp(self):
        UserType.objects.create(
            id = 1,
            name = "user"
        )

        user = User.objects.create(
                email = 'test1@test.com',
                password = 'pw12341234',
                name = 'tester1',
                user_type_id = 1
            )
    def tearDown(self):
        User.objects.filter(name='tester1').delete()

    def test_signin_post_success(self):
        data = {
            'email' : 'test1@test.com',
            'password' : 'pw12341234'
        }
        user = User.objects.get(email=data['email'])
        access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.post('/user/signin', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': '로그인 성공', 'access_token' : access_token})

    def test_siginin_post_fail_doesnotexist(self):
        data = {
            'email' : 'wrong@test.com',
            'password' : 'pw12341234'
        }
        response = client.post('/user/signin', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': '존재하지 않는 유저입니다'})

    def test_siginin_post_fail_wrong_password(self):
        data = {
            'email' : 'test1@test.com',
            'password' : 'pw123412341234'
        }
        response = client.post('/user/signin', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': '비밀번호가 잘못 입력되었습니다'})

    def test_siginin_post_fail_noinput_email(self):
        data = {
            'password' : 'pw12341234'
        }

        response = client.post('/user/signin', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': '이메일을 입력해주세요'})

    def test_siginin_post_fail_noinput_email(self):
        data = {
            'email' : 'test1@test.com'
        }
        response = client.post('/user/signin', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': '비밀번호를 입력해 주세요'})
