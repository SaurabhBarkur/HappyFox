from django.db import models
# Create your models here.

class Email(models.Model):
    email_id = models.IntegerField(unique=True)
    thread_id = models.IntegerField()
    email_from = models.CharField(max_length=400)
    email_to = models.CharField(max_length=400)
    date = models.DateTimeField()
    subject = models.TextField()
    body = models.TextField()

    @classmethod
    def get_model_fields(self):
        return [ field.name for field in self._meta.get_fields()]