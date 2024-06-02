from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, VerifyEmailSerializer
from django.utils.crypto import get_random_string
from django.core.mail import send_mail


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.otp_code = get_random_string(length=6, allowed_chars='0123456789')
        user.save()
        # send_mail(
        #     'Verify your email',
        #     f'Your OTP code is {user.otp_code}',
        #     'noreply@example.com',
        #     [user.email],
        #     fail_silently=False,
        # )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if not user.is_active:
                    return Response({'error': 'User account is disabled.'}, status=status.HTTP_400_BAD_REQUEST)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            try:
                user = User.objects.get(email=email, otp_code=otp_code)
                user.is_active = True
                user.otp_code = ''
                user.save()
                return Response({'success': 'Email verified successfully.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'Invalid OTP or email.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
