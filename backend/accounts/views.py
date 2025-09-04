from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import secrets

from .models import (
    User, Department, FacultyProfile, StudentProfile, 
    ParentProfile, ParentStudentRelationship, Invitation
)
from .serializers import (
    UserSerializer, DepartmentSerializer, FacultyProfileSerializer,
    StudentProfileSerializer, ParentProfileSerializer, 
    ParentStudentRelationshipSerializer, InvitationSerializer,
    LoginSerializer, RegistrationSerializer, PasswordChangeSerializer,
    FacultyProfileUpdateSerializer, StudentProfileUpdateSerializer,
    ParentProfileUpdateSerializer
)


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'


class IsFacultyUser(permissions.BasePermission):
    """
    Custom permission to only allow faculty users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'faculty'


class IsStudentUser(permissions.BasePermission):
    """
    Custom permission to only allow student users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'student'


class IsParentUser(permissions.BasePermission):
    """
    Custom permission to only allow parent users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'parent'


class LoginView(APIView):
    """
    User login endpoint
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    User logout endpoint
    """
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})


class RegistrationView(APIView):
    """
    User registration endpoint
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Registration successful',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    """
    Password change endpoint
    """
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'message': 'Password changed successfully'})
            else:
                return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentListCreateView(generics.ListCreateAPIView):
    """
    List and create departments (admin only)
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUser]


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete departments (admin only)
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUser]


class FacultyProfileListCreateView(generics.ListCreateAPIView):
    """
    List and create faculty profiles (admin only)
    """
    queryset = FacultyProfile.objects.all()
    serializer_class = FacultyProfileSerializer
    permission_classes = [IsAdminUser]


class FacultyProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete faculty profiles
    """
    queryset = FacultyProfile.objects.all()
    serializer_class = FacultyProfileSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser]
        return [permissions.IsAuthenticated]


class StudentProfileListCreateView(generics.ListCreateAPIView):
    """
    List and create student profiles (admin only)
    """
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAdminUser]


class StudentProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete student profiles
    """
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser]
        return [permissions.IsAuthenticated]


class ParentProfileListCreateView(generics.ListCreateAPIView):
    """
    List and create parent profiles (admin only)
    """
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer
    permission_classes = [IsAdminUser]


class ParentProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete parent profiles
    """
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser]
        return [permissions.IsAuthenticated]


class ParentStudentRelationshipListCreateView(generics.ListCreateAPIView):
    """
    List and create parent-student relationships (admin only)
    """
    queryset = ParentStudentRelationship.objects.all()
    serializer_class = ParentStudentRelationshipSerializer
    permission_classes = [IsAdminUser]


class ParentStudentRelationshipDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete parent-student relationships (admin only)
    """
    queryset = ParentStudentRelationship.objects.all()
    serializer_class = ParentStudentRelationshipSerializer
    permission_classes = [IsAdminUser]


class InvitationListCreateView(generics.ListCreateAPIView):
    """
    List and create invitations (admin only)
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        # Generate unique token
        token = secrets.token_urlsafe(32)
        # Set expiration (7 days from now)
        expires_at = timezone.now() + timedelta(days=7)
        
        serializer.save(
            invited_by=self.request.user,
            token=token,
            expires_at=expires_at
        )


class InvitationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete invitations (admin only)
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAdminUser]


class UserProfileView(APIView):
    """
    Get current user's profile
    """
    def get(self, request):
        user = request.user
        if user.role == 'faculty':
            try:
                profile = FacultyProfile.objects.get(user=user)
                serializer = FacultyProfileSerializer(profile)
            except FacultyProfile.DoesNotExist:
                return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        elif user.role == 'student':
            try:
                profile = StudentProfile.objects.get(user=user)
                serializer = StudentProfileSerializer(profile)
            except StudentProfile.DoesNotExist:
                return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        elif user.role == 'parent':
            try:
                profile = ParentProfile.objects.get(user=user)
                serializer = ParentProfileSerializer(profile)
            except ParentProfile.DoesNotExist:
                return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = UserSerializer(user)
        
        return Response(serializer.data)


class ProfileUpdateView(APIView):
    """
    Update current user's profile
    """
    def put(self, request):
        user = request.user
        if user.role == 'faculty':
            try:
                profile = FacultyProfile.objects.get(user=user)
                serializer = FacultyProfileUpdateSerializer(profile, data=request.data, partial=True)
            except FacultyProfile.DoesNotExist:
                return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        elif user.role == 'student':
            try:
                profile = StudentProfile.objects.get(user=user)
                serializer = StudentProfileUpdateSerializer(profile, data=request.data, partial=True)
            except StudentProfile.DoesNotExist:
                return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        elif user.role == 'parent':
            try:
                profile = ParentProfile.objects.get(user=user)
                serializer = ParentProfileUpdateSerializer(profile, data=request.data, partial=True)
            except ParentProfile.DoesNotExist:
                return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Profile updates not supported for admin users'}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def accept_invitation(request, token):
    """
    Accept invitation and create user account
    """
    try:
        invitation = Invitation.objects.get(token=token, status='pending')
        
        # Check if invitation has expired
        if invitation.expires_at < timezone.now():
            invitation.status = 'expired'
            invitation.save()
            return Response({'error': 'Invitation has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user account
        user_data = request.data
        user_data['role'] = invitation.role
        user_data['email'] = invitation.email
        
        serializer = RegistrationSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Mark invitation as accepted
            invitation.status = 'accepted'
            invitation.save()
            
            return Response({
                'message': 'Account created successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Invitation.DoesNotExist:
        return Response({'error': 'Invalid invitation token'}, status=status.HTTP_404_NOT_FOUND)
