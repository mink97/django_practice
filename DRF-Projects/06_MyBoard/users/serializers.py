from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password # 장고의 기본 패스워드 검증도구
from django.contrib.auth import authenticate # 장고의 기본 authenticate 함수. TokenAuth 방식으로 유저 인증

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator # 이메일 중복 방지를 위한 검증 도구

from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField( # 비밀번호 확인용 필드
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})
        return data
    
    def create(self, validated_data): # create 요청에 대해 create 메소드 오버라이딩, 유저 생성 및 토큰 생성
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
        # write_only=True로 설정하여 응답에 비밀번호가 포함되지 않도록 설정(클라->서버 역직렬화는 가능, 직렬화는 불가능)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError("Error: Unable to log in with provided credentials.")
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('nickname', 'position', 'subjects', 'image')