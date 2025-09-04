from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from scheduling.models import ClassSchedule, StudentGroup
from accounts.models import StudentProfile, FacultyProfile


class Attendance(models.Model):
    """
    Individual attendance records
    """
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
        ('half_day', 'Half Day'),
    ]
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_records')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    marked_by = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='marked_attendance')
    marked_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.class_schedule.subject.name} - {self.date} ({self.status})"
    
    class Meta:
        unique_together = ['student', 'class_schedule', 'date']
        ordering = ['-date', 'class_schedule__start_time']


class AttendanceSession(models.Model):
    """
    Attendance marking sessions for faculty
    """
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='attendance_sessions')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='attendance_sessions')
    date = models.DateField()
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.faculty.user.get_full_name()} - {self.class_schedule.subject.name} - {self.date}"
    
    class Meta:
        unique_together = ['faculty', 'class_schedule', 'date']
        ordering = ['-date', '-start_time']


class AttendanceReport(models.Model):
    """
    Generated attendance reports
    """
    REPORT_TYPE_CHOICES = [
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
        ('semester', 'Semester Report'),
        ('custom', 'Custom Period Report'),
    ]
    
    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='attendance_reports')
    start_date = models.DateField()
    end_date = models.DateField()
    generated_by = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='generated_reports')
    generated_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=500, blank=True)  # For PDF/Excel reports
    summary_data = models.JSONField(default=dict)  # Store report summary
    
    def __str__(self):
        return f"{self.name} - {self.student_group} - {self.start_date} to {self.end_date}"
    
    class Meta:
        ordering = ['-generated_at']


class AttendancePolicy(models.Model):
    """
    Attendance policies and rules
    """
    name = models.CharField(max_length=100)
    department = models.ForeignKey('accounts.Department', on_delete=models.CASCADE, related_name='attendance_policies')
    minimum_attendance_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Minimum attendance percentage required"
    )
    late_threshold_minutes = models.PositiveIntegerField(
        default=15,
        help_text="Minutes after start time to mark as late"
    )
    excused_absence_reasons = models.JSONField(
        default=list,
        help_text="List of valid reasons for excused absences"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.department.name}"
    
    class Meta:
        verbose_name_plural = 'Attendance Policies'
        ordering = ['department', 'name']


class AttendanceAlert(models.Model):
    """
    Alerts for low attendance
    """
    ALERT_TYPE_CHOICES = [
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('notification', 'Notification'),
    ]
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    subject = models.ForeignKey('scheduling.Subject', on_delete=models.CASCADE, related_name='attendance_alerts')
    current_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    required_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='resolved_alerts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject.name} - {self.alert_type}"
    
    class Meta:
        ordering = ['-created_at']


class AttendanceStatistics(models.Model):
    """
    Pre-calculated attendance statistics for performance
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_statistics')
    subject = models.ForeignKey('scheduling.Subject', on_delete=models.CASCADE, related_name='attendance_statistics')
    total_classes = models.PositiveIntegerField(default=0)
    classes_attended = models.PositiveIntegerField(default=0)
    classes_absent = models.PositiveIntegerField(default=0)
    classes_late = models.PositiveIntegerField(default=0)
    classes_excused = models.PositiveIntegerField(default=0)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject.name} - {self.attendance_percentage}%"
    
    class Meta:
        unique_together = ['student', 'subject']
        verbose_name_plural = 'Attendance Statistics'
        ordering = ['student', 'subject']


class BulkAttendance(models.Model):
    """
    Bulk attendance marking for efficiency
    """
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='bulk_attendance_sessions')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='bulk_attendance_sessions')
    date = models.DateField()
    attendance_data = models.JSONField(
        help_text="JSON data containing student_id: status mappings"
    )
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='verified_bulk_attendance', null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.faculty.user.get_full_name()} - {self.class_schedule.subject.name} - {self.date}"
    
    class Meta:
        unique_together = ['faculty', 'class_schedule', 'date']
        ordering = ['-date', '-created_at']
