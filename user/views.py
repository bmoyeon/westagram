import json
import bcrypt
import jwt

from django.views import View
from django.http import (
    HttpResponse,
    JsonResponse
)

from account.settings import (
    SECRET_KEY,
    ALGORITHM
)
from .models import User
from user.utils import check_user

class AccountView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : 'EMAIL_EXIST'}, status = 401)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            User.objects.create(
                email    = data['email'],
                password = hashed_password.decode('utf-8')
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class SigninView(View):
    @check_user
    def get(self, request):
        return JsonResponse({'user' : request.account.email}, status = 200)

    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = ALGORITHM)
                    return JsonResponse({'access_token' : access_token.decode('utf-8')}, status = 200)

                return JsonResponse({'message' : 'WRONG_PASSWORD'}, status = 401)
            return JsonResponse({'message' : 'WRONG_EMAIL'}, status = 401)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)
