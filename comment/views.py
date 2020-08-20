import json

from django.views import View
from django.http import (
    HttpResponse,
    JsonResponse
)

from .models import Comment
from user.models import User
from user.utils import check_user


class CommentView(View):
    @check_user
    def post(self, request):
        data = json.loads(request.body)

        try:
            Comment.objects.create(
                email   = request.account,
                comment = data['comment']
            )
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)
