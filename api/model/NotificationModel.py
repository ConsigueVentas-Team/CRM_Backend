from django.db import models
from api.model.UserModel import User

class Notification(models.Model):
    title = models.TextField(null=False)
    description = models.TextField(null=False)
    date = models.DateField()
    user_id =models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.pk
