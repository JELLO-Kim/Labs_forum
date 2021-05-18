import json, jwt

from django.views   import View
from django.http    import JsonResponse

from users.models   import User
from my_settings    import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        """[users] 일반 유저 회원가입
        Author:
            - Chae hyun Kim
        Args:
            - email
            - password
            - name
        Return:
            - 200: {'message' : '회원가입이 완료되었습니다.', 'result' : 새로가입한 유저의 이메일}
            - 400: 비밀번호는 8자 이상 입력해주세요.
            - 400: 특수문자는 @ ! ^ * 만 가능합니다.
            - 400: 이미 사용중인 이메일 입니다.
        """
        data = json.loads(request.body)
        email = data.get('email', None)
        password = data.get('password', None)
        name = data.get('name', None)

        # Key Validation
        if not email:
            return JsonResponse({'message' : '이메일을 입력해 주세요'}, status=400)
        if not password:
            return JsonResponse({'message' : '비밀번호를 입력해 주세요'}, status=400)
        if not name:
            return JsonResponse({'message' : '이름을 입력해 주세요'}, status=400)
        
        # 중복값 Validation
        if User.objects.filter(email=email).exists():
            return JsonResponse({'message' : '이미 사용중인 이메일입니다'}, status=400)
        
        # password 형식 Validation
        if len(password) < 8:
            return JsonResponse({'message' : '비밀번호는 8자 이상 입력해주세요'}, status=400)
        if password in "#":
            return JsonResponse({'message' : '특수문자는 @ ! ^ * 만 가능합니다'}, status=400)
        
        user = User.objects.create(
                email = email,
                password = password,
                name = name,
                user_type_id = 1
            )
        return JsonResponse({'message' : '회원가입 성공', 'result' : user.email}, status=201)

class SignInView(View):
    def post(self, request):
        """[users] email과 password로 로그인하기
        Author:
            - Chae hyun Kim
        Args:
            - email
            - password
        Returns:
            - 200: {'message' : '로그인 성공, 'access_token' : access_token}
            - 400: 존재하지 않는 유저입니다.
            - 400: 비밀번호를 다시 확인해주세요
        """

        data = json.loads(request.body)
        email = data.get('email', None)
        password = data.get('password', None)

        # Key Validation
        if not email:
            return JsonResponse({'message' : '이메일을 입력해 주세요'}, status=400)
        if not password:
            return JsonResponse({'message' : '비밀번호를 입력해 주세요'}, status=400)

        # 유저정보 유효성 Validation
        if not User.objects.filter(email=email).exists():
            return JsonResponse({'message' : '존재하지 않는 유저입니다'}, status=400)
        else:
            if data['password'] != User.objects.get(email=email).password:
                return JsonResponse({'message' : '비밀번호가 잘못 입력되었습니다'}, status=400)

        user = User.objects.get(email=email)
        access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)

        return JsonResponse({'message' : '로그인 성공', 'access_token' : access_token}, status=200)        