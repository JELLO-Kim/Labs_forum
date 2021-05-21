# Labs_forum
# About project

# Installation from the git repo
```bash
$ git clone https://github.com/JELLO-Kim/Labs_forum.git
$ cd Labs_forum
$ docker-compose up
```

<br>

# APIs

## 1. SignUp
- URL:
```bash
/users/signup
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
$ http POST localhost:8000/users/signup email="user@gmail.com" name="user" password="pw12341234"
```

- Success response:
  - Code : `201 (Created)`
  - Content : `{'message' : '회원가입 성공', 'result' : #새로가입한 유저의 이메일}`
- Error response:
  - Code : `400 (Bad request)`
  - Content : `{'message' : '이메일을 입력해 주세요'}`/`{'message' : '비밀번호를 입력해 주세요'}` <br>
              `{'message' : '이름을 입력해 주세요'}`/`{'message' : '이미 사용중인 이메일 입니다'}`<br>
              `{'message' : '8자 이상 입력해주세요'}` / `{'message' : '잘못된 형식의 이메일입니다'}`

<br>

## 2. SignIn
- URL:
```bash
/users/signin
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
$ http POST localhost:8000/users/signin email="user@gmail.com" password="pw12341234"
```

- Success response:
  - Code : `200 (Ok)`
  - Content : `{'message' : '로그인 성공', 'access_token' : #로그인 유저의 토큰}`
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
  - Content : `{'message' : 'SUCCESS', 'question_list' : #해당 조건의 모든 질문 목록들}`
- Error response:
  - Situation : Invalid question type id
  - Code : `400 (Bad request)`
  - Content : `{'message' : '유효하지 않은 질문 타입입니다.'}`

<br>

## 4. Create new question
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

- Sample call:
```bash
$ http POST localhost:8000/questions/1
```

- Success response:
  - Code : `201 (Created)`
  - Content : `{'message' : '새 질문이 등록되었습니다', 'result' : #새로 작성된 질문의 제목}`
- Error response:
  - Situation : Key Error
  - Code : `400 (Bad request)`
  - Content : `{'message' : '질문 제목을 입력해주세요'}`/`{'message' : '질문 내용을 채워주세요'}`

<br>

## 5. Delete one question (hard_delete)
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
$ http DELETE localhost:8000/questions
```

- Success response:
  - Code : `204 (Deleted)`
  - Content : `{'message' : 'DELETE'}`

- Error response:
  - Situation : Invalid question_id 
  - Code : `404 (Not found)`
  - Content : `{'message' : '존재하지 않는 질문입니다'}`
  - Situation : Forbiddend (no writter)
  - Code : `403 (Not found)`
  - Content : `{'message' : '권한이 없습니다'}`

<br>

## 6. Edit one question
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
$ http PATCH localhost:8000/questions
```

- Success response:
  - Code : `200 (Ok)`
  - Content : `{'message' : '수정이 완료되었습니다'}`

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
  - Content : `{'message' : '삭제처리 되었습니다'}`

- Error response:
  - Situation : Invalid question_id 
  - Code : `404 (Not found)`
  - Content : `{'message' : '존재하지 않는 질문입니다'}`
  - Situation : Already soft_deleted question
  - Code : `404 (Not found)`
  - Content : `{'message' : '이미 삭제된 질문입니다'}`

<br>

## 8. Show all comments of one question
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
  - Content : `{'message' : 'SUCCESS', 'comment_list' : #질문의 답변리스트}`

- Error response:
  - Situation : Invalid question_id 
  - Code : `404 (Not found)`
  - Content : `{'message' : '존재하지 않는 질문입니다'}`
  - Situation : Already soft_deleted question
  - Code : `400 (Bad request)`
  - Content : `{'message' : '삭제된 게시물입니다'}`

<br>

## 9. Create new comments on one question
```bash
/questions/<int:question_id>/comments
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
$ http GET localhost:8000/questions/1/comments
```

- Success response:
  - Code : `200 (Ok)`
  - Content : `{'message' : 'SUCCESS', 'comment_list' : #질문의 답변리스트}`

- Error response:
  - Situation : Invalid question_id 
  - Code : `404 (Not found)`
  - Content : `{'message' : '존재하지 않는 질문입니다'}`
  - Situation : Already soft_deleted question
  - Code : `400 (Bad request)`
  - Content : `{'message' : '삭제된 게시물입니다'}`
