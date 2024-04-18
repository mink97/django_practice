from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from .models import Profile
from .permissions import CustomReadOnly

# Create your views here.
class RegisterView(generics.CreateAPIView): # CreateAPIView를 상속받아서 사용자 생성 뷰 생성
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView): # 모델에 영향 x, 기본 제공되는 APIView를 상속받아서 로그인 뷰 생성
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data) # get_serializer()는 CreateAPIView의 메소드
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data # validate()의 리턴값
        return Response({
            "token": token.key,
        }, status=status.HTTP_200_OK)
    
class ProfileView(generics.RetrieveUpdateAPIView): # 가져오기 기능 + 수정 기능
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [CustomReadOnly] # CustomReadOnly 클래스를 사용하여 권한 설정