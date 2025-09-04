from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model with role-based access control
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # Override username to use email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Department(models.Model):
    """
    Academic departments
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        ordering = ['name']


class FacultyProfile(models.Model):
    """
    Extended profile for faculty members
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty_members')
    designation = models.CharField(max_length=50)
    qualification = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='faculty_profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation}"
    
    class Meta:
        verbose_name = 'Faculty Profile'
        verbose_name_plural = 'Faculty Profiles'


class StudentProfile(models.Model):
    """
    Extended profile for students
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    year_of_admission = models.PositiveIntegerField()
    current_year = models.PositiveIntegerField(default=1)
    semester = models.PositiveIntegerField(default=1)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"
    
    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'


class ParentProfile(models.Model):
    """
    Extended profile for parents
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    relationship = models.CharField(max_length=20)  # Father, Mother, Guardian
    occupation = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.relationship}"
    
    class Meta:
        verbose_name = 'Parent Profile'
        verbose_name_plural = 'Parent Profiles'


class ParentStudentRelationship(models.Model):
    """
    Links parents to their children (students)
    """
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='children')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='parents')
    is_primary_contact = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.parent.user.get_full_name()} - {self.student.user.get_full_name()}"
    
    class Meta:
        unique_together = ['parent', 'student']
        verbose_name = 'Parent-Student Relationship'
        verbose_name_plural = 'Parent-Student Relationships'


class Invitation(models.Model):
    """
    Email invitations for new users
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('expired', 'Expired'),
    ]
    
    email = models.EmailField()
    role = models.CharField(max_length=10, choices=User.ROLE_CHOICES)
    token = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email} - {self.get_role_display()}"
    
    class Meta:
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'
