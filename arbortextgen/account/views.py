from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import StudentSerializer
from .models import Student

class RegisterStudentAPIView(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            refresh = RefreshToken.for_user(student)
            return Response({
                "message": "Student registered successfully",
                "user_id": student.id,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        if not student.check_password(password):
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(student)

        response = Response({
            'id': student.id,
            'username': student.username,
            'email': student.email,
            'grade': student.grade,  # Include grade
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_200_OK)

        response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=True, samesite='Lax')
        response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True, samesite='Lax')

        return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    refresh_token = request.data.get('refresh_token') or request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({'error': 'Refresh token is missing'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh_token = RefreshToken(refresh_token)
        return Response({'access_token': str(refresh_token.access_token)})
    except TokenError:
        return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    def get(self, request):
        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        refresh_token = request.COOKIES.get('refresh_token')

        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')

        try:
            if refresh_token:
                RefreshToken(refresh_token).blacklist()
        except Exception:
            pass

        return response
