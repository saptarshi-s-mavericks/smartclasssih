from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Department, FacultyProfile, StudentProfile, 
    ParentProfile, ParentStudentRelationship, Invitation
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'first_name', 'last_name', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'designation', 'experience_years')
    list_filter = ('department', 'designation')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'employee_id')
    ordering = ('user__first_name',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'roll_number', 'department', 'current_year', 'semester')
    list_filter = ('department', 'current_year', 'semester', 'gender')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'student_id', 'roll_number')
    ordering = ('user__first_name',)


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'relationship', 'occupation', 'emergency_contact')
    list_filter = ('relationship',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('user__first_name',)


@admin.register(ParentStudentRelationship)
class ParentStudentRelationshipAdmin(admin.ModelAdmin):
    list_display = ('parent', 'student', 'is_primary_contact', 'created_at')
    list_filter = ('is_primary_contact', 'created_at')
    search_fields = ('parent__user__email', 'student__user__email')
    ordering = ('-created_at',)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'status', 'invited_by', 'expires_at', 'created_at')
    list_filter = ('role', 'status', 'created_at')
    search_fields = ('email', 'invited_by__email')
    ordering = ('-created_at',)
    readonly_fields = ('token', 'created_at')
