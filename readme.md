# 빠르게 해보기 

## 시작하기전 해야할 것

django 에 데이터를 자동으로 넣을 것이기 때문에 다음을 반드시 한다.

- 가급적 virtualenv 환경을 설정한다.
- pip install --upgrade pip
- pip install -r requirements.txt
- ./manage.py migrate
- ./manage.py createsuperuser
- ./manage.py runserver 0.0.0.0:8000
- 브라우져로 http://localhost:8000 을 열고 로그인 한 후 ThePress 객체를 하나 생성한다.

## 일단 급해서 작성

다음으로 listing_news 로 url 을 얻오는 것을 시뮬레이션 할 수 있다.

- ./manage.py listing_news
