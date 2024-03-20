from rest_framework import serializers
from .models import Meatings
from accounts.models import CustomUser


class MeatingSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(is_tutor=True))
    class Meta:
        model = Meatings
        fields = ['id', 'meating_name', 'content', 'time', 'tutor']