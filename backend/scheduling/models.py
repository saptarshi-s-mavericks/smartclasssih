from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User, Department, FacultyProfile, StudentProfile


class Subject(models.Model):
    """
    Academic subjects/courses
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    credits = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        ordering = ['name']


class Room(models.Model):
    """
    Classrooms and facilities
    """
    ROOM_TYPE_CHOICES = [
        ('classroom', 'Classroom'),
        ('lab', 'Laboratory'),
        ('auditorium', 'Auditorium'),
        ('seminar', 'Seminar Hall'),
        ('conference', 'Conference Room'),
    ]
    
    name = models.CharField(max_length=50)
    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='classroom')
    capacity = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='rooms', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    facilities = models.TextField(blank=True)  # Projector, AC, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.room_number})"
    
    class Meta:
        ordering = ['room_number']


class TimeSlot(models.Model):
    """
    Available time slots for scheduling
    """
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_day_display()} {self.start_time} - {self.end_time}"
    
    class Meta:
        unique_together = ['day', 'start_time', 'end_time']
        ordering = ['day', 'start_time']


class ClassSchedule(models.Model):
    """
    Individual class sessions
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classes')
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='classes')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='classes')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='classes')
    day = models.CharField(max_length=10, choices=TimeSlot.DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subject.name} - {self.faculty.user.get_full_name()} - {self.room.name}"
    
    class Meta:
        unique_together = ['room', 'day', 'start_time']
        ordering = ['day', 'start_time']


class StudentGroup(models.Model):
    """
    Groups of students (classes, sections)
    """
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='student_groups')
    year = models.PositiveIntegerField()
    section = models.CharField(max_length=5)
    students = models.ManyToManyField(StudentProfile, related_name='groups')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.department.name} - Year {self.year} - Section {self.section}"
    
    class Meta:
        unique_together = ['department', 'year', 'section']
        ordering = ['department', 'year', 'section']


class GroupSchedule(models.Model):
    """
    Schedule for student groups
    """
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='schedules')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='group_schedules')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.group} - {self.class_schedule}"
    
    class Meta:
        unique_together = ['group', 'class_schedule']


class SchedulingConstraint(models.Model):
    """
    Constraints for timetable generation
    """
    CONSTRAINT_TYPE_CHOICES = [
        ('faculty_availability', 'Faculty Availability'),
        ('room_capacity', 'Room Capacity'),
        ('subject_prerequisite', 'Subject Prerequisite'),
        ('time_conflict', 'Time Conflict'),
        ('department_preference', 'Department Preference'),
    ]
    
    name = models.CharField(max_length=100)
    constraint_type = models.CharField(max_length=30, choices=CONSTRAINT_TYPE_CHOICES)
    description = models.TextField()
    is_hard_constraint = models.BooleanField(default=True)  # Hard vs Soft constraint
    weight = models.PositiveIntegerField(default=1)  # For soft constraints
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_constraint_type_display()})"
    
    class Meta:
        ordering = ['constraint_type', 'name']


class FacultyAvailability(models.Model):
    """
    Faculty availability for scheduling
    """
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='availability')
    day = models.CharField(max_length=10, choices=TimeSlot.DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    reason = models.CharField(max_length=200, blank=True)  # For unavailability
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        status = "Available" if self.is_available else "Unavailable"
        return f"{self.faculty.user.get_full_name()} - {self.get_day_display()} {self.start_time}-{self.end_time} ({status})"
    
    class Meta:
        unique_together = ['faculty', 'day', 'start_time']


class Timetable(models.Model):
    """
    Generated timetables
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
    ]
    
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='timetables')
    academic_year = models.CharField(max_length=10)  # e.g., "2024-25"
    semester = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_timetables')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_timetables', null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.department.name} - {self.academic_year} Sem {self.semester}"
    
    class Meta:
        unique_together = ['department', 'academic_year', 'semester']
        ordering = ['-created_at']


class TimetableEntry(models.Model):
    """
    Individual entries in a timetable
    """
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='entries')
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='timetable_entries')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='timetable_entries')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.timetable.name} - {self.group} - {self.class_schedule}"
    
    class Meta:
        unique_together = ['timetable', 'group', 'class_schedule']


class SchedulingRequest(models.Model):
    """
    Requests for schedule changes
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    REQUEST_TYPE_CHOICES = [
        ('change_time', 'Change Time'),
        ('change_room', 'Change Room'),
        ('add_class', 'Add Class'),
        ('remove_class', 'Remove Class'),
        ('swap_classes', 'Swap Classes'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheduling_requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='scheduling_requests')
    current_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='change_requests', null=True, blank=True)
    proposed_day = models.CharField(max_length=10, choices=TimeSlot.DAY_CHOICES, blank=True)
    proposed_start_time = models.TimeField(null=True, blank=True)
    proposed_end_time = models.TimeField(null=True)
    proposed_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='scheduling_requests', null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_requests', null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.requester.get_full_name()} - {self.get_request_type_display()} - {self.subject.name}"
    
    class Meta:
        ordering = ['-created_at']
