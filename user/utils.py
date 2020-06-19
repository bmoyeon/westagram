import jwt
import json

from django.http import JsonResponse

from account.settings import SECRET_KEY
from user.models import User

def check_user(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)	# 토큰 가져옴

        if access_token is None:        #토큰이 없는 경우
            return JsonResponse({"message":"INVALID_TOKEN"}, status=400)

        try:
            user_id = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')	#토큰 디코드
            account = User.objects.get(id=user_id['id'])	#정보 가져오기
            request.account = account	#request에 account값 주기

            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({"message":"unknown_user"}, status=401)

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message":"invalid_token"}, status=401)

    return wrapper