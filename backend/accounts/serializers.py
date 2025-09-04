from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    User, Department, FacultyProfile, StudentProfile, 
    ParentProfile, ParentStudentRelationship, Invitation
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'role', 'phone', 'is_active', 'date_joined')
        read_only_fields = ('id', 'is_active', 'date_joined')


class FacultyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = FacultyProfile
        fields = '__all__'


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = StudentProfile
        fields = '__all__'


class ParentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ParentProfile
        fields = '__all__'


class ParentStudentRelationshipSerializer(serializers.ModelSerializer):
    parent = ParentProfileSerializer(read_only=True)
    student = StudentProfileSerializer(read_only=True)
    parent_id = serializers.IntegerField(write_only=True)
    student_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ParentStudentRelationship
        fields = '__all__'


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'
        read_only_fields = ('token', 'status', 'invited_by', 'created_at')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password.')


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirm', 'first_name', 'last_name', 'role')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = None  # Will be set in subclasses
        fields = '__all__'
    
    def update(self, instance, validated_data):
        # Update user fields if provided
        user_data = validated_data.pop('user', {})
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        
        # Update profile fields
        return super().update(instance, validated_data)


class FacultyProfileUpdateSerializer(ProfileUpdateSerializer):
    class Meta(ProfileUpdateSerializer.Meta):
        model = FacultyProfile


class StudentProfileUpdateSerializer(ProfileUpdateSerializer):
    class Meta(ProfileUpdateSerializer.Meta):
        model = StudentProfile


class ParentProfileUpdateSerializer(ProfileUpdateSerializer):
    class Meta(ProfileUpdateSerializer.Meta):
        model = ParentProfile
