from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from accounts.models import CustomUser,StudentProfile,TutorProfile
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

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

    def validate_password(self, value):
        validate_password(value) 
        return value

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
        print(validated_data,"this is the validated data")
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
    




class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile_image', 'is_tutor', 'date_of_birth', 'gender', 'is_tutor_verify']


class TutorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorProfile
        fields = ['tutor', 'qualification', 'certificate']  

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['student', 'courses']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'date_of_birth', 'gender', 'is_tutor']



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to login with provided credentials.")
        else:
            raise serializers.ValidationError("Must provide username and password.")

        return data