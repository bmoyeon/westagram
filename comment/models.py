from django.db import models
from user.models import User

class Comment(models.Model):
    email      = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    comment    = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'comments'
