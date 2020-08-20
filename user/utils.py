import jwt
import json

from django.http import JsonResponse

from account.settings import (
    SECRET_KEY,
    ALGORITHM
)
from user.models import User

def check_user(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)

        if access_token is None:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)

        try:
            user_id = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')['id']
            account = User.objects.get(id = user_id)
            request.account = account

            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({"message" : "unknown_user"}, status = 401)

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "invalid_token"}, status = 401)

    return wrapper
