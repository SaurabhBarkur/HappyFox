from .models import Email
from rest_framework import serializers


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('email_id', 'thread_id', 'email_from', 'email_to', 'date', 'subject')