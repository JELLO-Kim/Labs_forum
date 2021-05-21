# Labs_forum
Project for "모두의 연구소"
<br>

# API abbstract
- SignUp / SignIn
- Read Question list
- Create new question
- Edit one question
- Delete one question (soft_delete)
- Delete soem questions (hard_delete)
- Read commens of one question
- Create new comment
- Create or Delete question_like relationship
- Read best question of specific month

<br>

# Installation from the git repo
```bash
$ git clone https://github.com/JELLO-Kim/Labs_forum.git
$ cd Labs_forum
$ docker-compose up
```

<br>

# Setting info

#### my_settings.py
- SECRET_KEY for JWT and Django's SECRET_KEY
- Algorithm for JWT
- DATABASE information

#### requirements.txt
- need to intallation python modules


<br>

# Project Structure
```bash
.
├── Dockerfile
├── README.md
├── requirements.txt
├── utils.py
├── wait-for-it.sh
├── data
│   └── forum.sql
├── docker-compose.yml
├── forum
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── questions
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└──users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py

```
# APIs

## 1. SignUp
- URL:
```bash
/user/signup
```
- Method:
```bash
POST
```

- Body required:
```bash
email, password, name
```

- Sample call:
```bash
$ http POST localhost:8000/user/signup email="user1@gmail.com" name="user1" password="pw12341234"
```

- Success response:
  - Code : `201 (Created)`
  - Content : `{
    "message": "회원가입 성공",
    "result": "user1@gmail.com"
}`
- Error response:
  - Code : `400 (Bad request)`
  - Content : `{'message' : '이메일을 입력해 주세요'}`/`{'message' : '비밀번호를 입력해 주세요'}` <br>
              `{'message' : '이름을 입력해 주세요'}`/`{'message' : '이미 사용중인 이메일 입니다'}`<br>
              `{'message' : '8자 이상 입력해주세요'}` / `{'message' : '잘못된 형식의 이메일입니다'}`

<br>

## 2. SignIn
- URL:
```bash
/user/signin
```
- Method:
```bash
POST
```

- Body required:
```bash
email, password
```

- Sample call:
```bash
$ http POST localhost:8000/user/signin email="cogus950403@gmail.com" password="pw12341234"
```

- Success response:
  - Code : `200 (Ok)`
  - Content : `{
    "message": "로그인 성공",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.MN9OkseOwzcb7lFyO2fa70_kTWN6C3aqNYCvZOHNEvQ"
}`
- Error response:
  - Code : `400 (Bad request)`
  - Content : `{'message' : '이메일을 입력해 주세요'}`/`{'message' : '비밀번호를 입력해 주세요'}` <br>
              `{'message' : '존재하지 않는 유저입니다'}`/`{'message' : '비밀번호가 잘못 입력되었습니다'}`

<br>

## 3. Show all questions / filtering by category / search by keyword
- URL:
```bash
/questions
```
- Method:
```bash
GET
```
- URL quary parameter (Optional):
```bash
keyword=<String>
type=<Int:question_type_id>
```

- Sample call:
```bash
$ http GET localhost:8000/questions
$ http GET localhost:8000/questions keyword=="date"
$ http GET localhost:8000/questions type==1
```

- Success response:
  - Code : `200 (Ok)`
  - Content : `{
    "message": "SUCCESS",
    "question_list": [
        {
            "title": "1번질문",
            "content": "1번질문내용",
            "created_at": "2021-04-03 00:00:00",
            "question_type": "기타",
            "writter": "cogus",
            "like_num": 0
        },
        {
            "title": "2번질문",
            "content": "2번질문내용",
            "created_at": "2021-05-21 20:01:10",
            "question_type": "계정",
            "writter": "cogus",
            "like_num": 2
        },
        {
            "title": "3번질문_date",
            "content": "3번질문내용",
            "created_at": "2021-05-21 20:03:38",
            "question_type": "기타",
            "writter": "cogus",
            "like_num": 3
        }
    ]
}`
 - Situation : Search by keyword (date)
 - Code : `200 (Ok)`
 - Content : `{
    "message": "SUCCESS",
    "question_list": [
        {
            "title": "3번질문_date",
            "content": "3번질문내용",
            "created_at": "2021-05-21 20:03:38",
            "question_type": "기타",
            "writter": "cogus",
            "like_num": 3
        }
    ]
}`
 - Situation : Filtering by category (question_type_id=1)
 - Code : `200 (Ok)`
 - Content : `{
    "message": "SUCCESS",
    "question_list": [
        {
            "title": "2번질문",
            "content": "2번질문내용",
            "created_at": "2021-05-21 20:01:10",
            "question_type": "계정",
            "writter": "cogus",
            "like_num": 2
        }
    ]
}`
- Error response:
  - Situation : Invalid question type id
  - Code : `400 (Bad request)`
  - Content : `{'message' : '유효하지 않은 질문 타입입니다.'}`

<br>

## 4. Create new question
- URL:
```bash
/questions
```
- Method:
```bash
POST
```
- Body required:
```bash
title, content, question_type
```
 +) question_type is optional, if no input, it will be setted "기타" category (id=1)

- Sample call:
```bash
$ http POST localhost:8000/questions/1 title="2번질문", content="2번질문내용
$ http POST localhost:8000/questions/1 title="3번질문_date", content="3번질문내용", question_type=2
```

- Success response:
  - Code : `201 (Created)`
  - Content : `{
    "message": "새 질문이 등록되었습니다",
    "result": "2번질문"
}`
  - Code : `201 (Created)`
  - Content : `{
    "message": "새 질문이 등록되었습니다",
    "result": "3번질문_date"
}}`
- Error response:
  - Situation : Key Error
  - Code : `400 (Bad request)`
  - Content : `{'message' : '질문 제목을 입력해주세요'}`/`{'message' : '질문 내용을 채워주세요'}`

<br>

## 5. Delete one question (hard_delete)
- URL:
```bash
/questions
```
- Method:
```bash
DELETE
```

- Body requires:
```bash
question_id==[#삭제할 질문의 id가 담긴 list]
```

- Sample call:
```bash
$ http DELETE localhost:8000/questions question_id=[4]
```

- Success response:
  - Code : `204 (Deleted)`
  - Content : `{
    "message": "DELETE"
}`

- Error response:
  - Situation : Invalid question_id 
  - Code : `404 (Not found)`
  - Content : `{'message' : '존재하지 않는 질문입니다'}`
  - Situation : Forbiddend (no writter)
  - Code : `403 (Not found)`
  - Content : `{'message' : '권한이 없습니다'}`

<br>

## 6. Edit one question
- URL:
```bash
/questions/<int:question_id>
```
- Method:
```bash
PATCH
```
- URL required:
```bash
question_id = <Int>
```

- Body required (Optional):
```bash
title, content, question_type
```

- Sample call:
```bash
$ http PATCH localhost:8000/questions question_type_id=2
```

- Success response:
  - Code : `200 (Ok)`
  - Content : `{
    "message": "수정이 완료되었습니다"
}`

- Error response:
  - Situation : non login_user
  - Code : `401 (Unathorized)`
  - Content : `{'message' : '로그인후 이용해 주세요'}` <br>

  - Situation : permission denied (no writter)
  - Code : `403 (Forbiddend)`
  - Content : `{'message' : '권한이 없습니다'}` <br>

  - Situation : Invalid question_id 
  - Code : `404 (Not found)`
  - Content : `{'message' : '존재하지 않는 질문입니다'}`/`{'message' : '이미 삭제된 질문입니다'}`

<br>

## 7. Delete one question (soft_delete)
- URL:
```bash
/questions/<int:question_id>
```
- Method:
```bash
DELETE
```
- URL required:
```bash
question_id = <Int>
```

- URL quary parameter (essentail):
```bash
question_id=<Int>
```

- Sample call:
```bash
$ http DELETE localhost:8000/questions/1
```

- Success response:
  - Code : `200 (Ok)`
  - Content : `{
    "message": "삭제처리 되었습니다"
}`

- Error response:
  - Situation : Invalid question_id 
  - Code : `404 (Not found)`
  - Content : `{'message' : '존재하지 않는 질문입니다'}`
  - Situation : Already soft_deleted question
  - Code : `404 (Not found)`
  - Content : `{'message' : '이미 삭제된 질문입니다'}`

<br>

## 8. Show all comments of one question
- URL:
```bash
/questions/<int:question_id>/comments
```
- Method:
```bash
GET
```

- URL requires:
```bash
question_id = <Int>
```

- Sample call:
```bash
$ http GET localhost:8000/questions/1/comments
```

- Success response:
  - Code : `200 (Ok)`
  - Content : `{
    "message": "SUCCESS",
    "comment_list": [
        {
            "writter": "user1",
            "quetion_id": 1,
            "comment": "질문1에 대한 답변1입니다",
            "is_parent": null,
            "created_at": "2021-05-21 20:21:09"
        },
        {
            "writter": "purple",
            "quetion_id": 1,
            "comment": "질문1에 대한 답변2입니다",
            "is_parent": null,
            "created_at": "2021-05-21 20:21:39"
        },
        {
            "writter": "cogus",
            "quetion_id": 1,
            "comment": "질문1의 답변1에 대한 대댓글입니다",
            "is_parent": 1,
            "created_at": "2021-05-21 20:22:43"
        }
    ]
}`

- Error response:
  - Situation : Invalid question_id 
  - Code : `404 (Not found)`
  - Content : `{'message' : '존재하지 않는 질문입니다'}`
  - Situation : Already soft_deleted question
  - Code : `400 (Bad request)`
  - Content : `{'message' : '삭제된 게시물입니다'}`

<br>

## 9. Create new comments on one question
- URL:
```bash
/questions/<int:question_id>/comments"
```
- Method:
```bash
POST
```

- URL requires:
```bash
question_id = <Int>
```

- Body requires:
```bash
comment = <String>
is_parent = <Int>
```
+) `is_parent` is optional

- Sample call:
```bash
$ http POST localhost:8000/questions/1/comments comment="질문1에 대한 답변2입니다"
```

- Success response:
  - Code : `201 (Created)`
  - Content : `{
    "message": "댓글이 등록되었습니다"
}`

- Error response:
  - Situation : Already soft_deleted question
  - Code : `400 (Bad request)`
  - Content : `{'message' : '삭제된 게시물입니다'}`
  - Situation : Key Error
  - Code : `400 (Bad request)`
  - Content : `{'message' : '내용을 입력해 주세요'}`

<br>

## 10. Question Like (Create & Delete)
- URL:
```bash
/questions/like
```
- Method:
```bash
POST
```

- Body requires:
```bash
question_id = <Int:question_id>
```
+) `is_parent` is optional

- Sample call:
```bash
$ http POST localhost:8000/questions/like question_id=1
```

- Success response:
  - Situation : Create Like
  - Code : `201 (Created)`
  - Content : `{
    "message": "좋아요가 등록되었습니다"
}`
  - Situation : Cancle Like
  - Code : `200 (Ok)`
  - Content : `{
    "message": "좋아요가 쥐소되었습니다"
}`

- Error response:
  - Situation : Already soft_deleted question
  - Code : `400 (Bad request)`
  - Content : `{'message' : '삭제된 게시물입니다'}`
  - Situation : Invalid question_id
  - Code : `400 (Bad request)`
  - Content : `{'message' : '존재하지 않는 질문입니다'}`

<br>

## 10. Best Question
- URL:
```bash
/questions/best/<int:question_id>
```
- Method:
```bash
GET
```

- URL quary parameter requires:
```bash
question_id = <Int:question_id>
```

- Sample call:
```bash
$ http POST localhost:8000/questions/best/2
```

- Success response:
  - Situation : SUCCESS
  - Code : `200 (Ok)`
  - Content : `{
    "message": "SUCCESS",
    "best_question": {
        "writter": "cogus",
        "question_type": "기타",
        "title": "3번질문_date",
        "content": "3번질문내용",
        "created_at": "2021-05-21"
    }
}`
  - Situation : No data Exsits (not wrong)
  - Code : `200 (Ok)`
  - Content : `{'message' : '해당하는 조건이 없습니다'}`

- Error response:
  - Situation : Already soft_deleted question
  - Code : `400 (Bad request)`
  - Content : `{'message' : '삭제된 게시물입니다'}`
  - Situation : Invalid question_id
  - Code : `400 (Bad request)`
  - Content : `{'message' : '존재하지 않는 질문입니다'}`
