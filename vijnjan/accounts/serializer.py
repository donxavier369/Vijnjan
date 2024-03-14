from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from accounts.models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only = True)#used for input (registration) but not included in the response.write_only
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="Username already exists.")]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="Email already exists.")]
    )
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum(): # check alphanumeric
            raise serializers.ValidationError(
                self.default_error_messages
            )
        print("this is attrs:",attrs)
        return attrs
    
    def create(self, validated_data):
        print(validated_data,"this is the validate data")
        # return User.objects.create(**validated_data)
        password = validated_data['password']
        hashed_password = make_password(password)
        user = CustomUser.objects.create(
            email = validated_data['email'],
            username = validated_data['username'],
            password = hashed_password
        )
        user.save()
        return user
    

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print(user,"user")
        token = super().get_token(user)
        token['superuser'] = user.is_superuser
        token['name'] = user.username
        token['email'] = user.email
        token['is_active'] = user.is_active
        return token