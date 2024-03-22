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
        fields = ['id', 'email', 'username', 'date_of_birth', 'gender', 'password', 'is_tutor']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        date_of_birth = attrs.get('date_of_birth','')
        gender = attrs.get('gender', '')
        is_tutor = attrs.get('is_tutor', '')

        # Check if the username contains any invalid characters
        if any(char in username for char in r'~!@#$%^&*()+=\|{}[]:;"\'<>?,./'):
            raise serializers.ValidationError("Username cannot contain special characters other than spaces.")

        return attrs

    
    def create(self, validated_data):
        print(validated_data,"this is the validate data")
        # return User.objects.create(**validated_data)
        password = validated_data['password']
        hashed_password = make_password(password)
        user = CustomUser.objects.create(
            email = validated_data['email'],
            username = validated_data['username'],
            date_of_birth = validated_data['date_of_birth'],
            gender = validated_data['gender'],
            password = hashed_password,
            is_tutor = validated_data['is_tutor']
        )
        user.save()
        return user
    

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print(user,"user")
        token = super().get_token(user)
        token['id'] = user.id
        token['superuser'] = user.is_superuser
        token['tutor'] = user.is_tutor
        token['name'] = user.username
        token['email'] = user.email
        token['is_active'] = user.is_active
        return token