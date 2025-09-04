from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from scheduling.models import Subject, StudentGroup
from accounts.models import StudentProfile, FacultyProfile


class Exam(models.Model):
    """
    Examination definitions
    """
    EXAM_TYPE_CHOICES = [
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('practical', 'Practical'),
        ('seminar', 'Seminar'),
    ]
    
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='exams')
    total_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
    exam_date = models.DateField()
    start_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    instructions = models.TextField(blank=True)
    created_by = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='created_exams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject.name} - {self.student_group}"
    
    class Meta:
        ordering = ['-exam_date', 'start_time']


class ExamResult(models.Model):
    """
    Individual student exam results
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='exam_results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, blank=True)
    remarks = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    published_by = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='published_results', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.name} - {self.marks_obtained}/{self.exam.total_marks}"
    
    class Meta:
        unique_together = ['student', 'exam']
        ordering = ['-created_at']


class Grade(models.Model):
    """
    Grade definitions
    """
    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
        ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
        ('D+', 'D+'), ('D', 'D'), ('D-', 'D-'),
        ('F', 'F'),
    ]
    
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, unique=True)
    min_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    max_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade_points = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.CharField(max_length=100)
    is_pass = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.grade} ({self.min_percentage}% - {self.max_percentage}%)"
    
    class Meta:
        ordering = ['grade_points']


class SubjectGrade(models.Model):
    """
    Final subject grades for students
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='subject_grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='student_grades')
    academic_year = models.CharField(max_length=10)
    semester = models.PositiveIntegerField()
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subject_grades')
    grade_points = models.DecimalField(max_digits=3, decimal_places=1)
    is_pass = models.BooleanField(default=True)
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject.name} - {self.grade.grade}"
    
    class Meta:
        unique_together = ['student', 'subject', 'academic_year', 'semester']
        ordering = ['student', 'subject', 'academic_year', 'semester']


class AcademicPerformance(models.Model):
    """
    Overall academic performance metrics
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='academic_performance')
    academic_year = models.CharField(max_length=10)
    semester = models.PositiveIntegerField()
    total_credits = models.PositiveIntegerField(default=0)
    earned_credits = models.PositiveIntegerField(default=0)
    total_grade_points = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    sgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    rank_in_class = models.PositiveIntegerField(null=True, blank=True)
    total_students = models.PositiveIntegerField(default=0)
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.academic_year} Sem {self.semester} - CGPA: {self.cgpa}"
    
    class Meta:
        unique_together = ['student', 'academic_year', 'semester']
        verbose_name_plural = 'Academic Performance'
        ordering = ['student', 'academic_year', 'semester']


class Assignment(models.Model):
    """
    Academic assignments
    """
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='assignments')
    description = models.TextField()
    total_marks = models.PositiveIntegerField()
    due_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='created_assignments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject.name} - {self.student_group}"
    
    class Meta:
        ordering = ['-due_date']


class AssignmentSubmission(models.Model):
    """
    Student assignment submissions
    """
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('late', 'Late'),
        ('not_submitted', 'Not Submitted'),
    ]
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='assignment_submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    file_path = models.CharField(max_length=500, blank=True)
    comments = models.TextField(blank=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='graded_submissions', null=True, blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.assignment.name}"
    
    class Meta:
        unique_together = ['student', 'assignment']
        ordering = ['-submitted_at']


class AcademicCalendar(models.Model):
    """
    Academic calendar events
    """
    EVENT_TYPE_CHOICES = [
        ('holiday', 'Holiday'),
        ('exam', 'Examination'),
        ('assignment', 'Assignment Due'),
        ('event', 'Academic Event'),
        ('break', 'Break'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.start_date} to {self.end_date}"
    
    class Meta:
        ordering = ['start_date']


class PerformanceReport(models.Model):
    """
    Generated performance reports
    """
    REPORT_TYPE_CHOICES = [
        ('individual', 'Individual Student Report'),
        ('class', 'Class Performance Report'),
        ('subject', 'Subject Performance Report'),
        ('comparative', 'Comparative Analysis Report'),
    ]
    
    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='performance_reports', null=True, blank=True)
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='performance_reports', null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='performance_reports', null=True, blank=True)
    academic_year = models.CharField(max_length=10)
    semester = models.PositiveIntegerField()
    generated_by = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='generated_performance_reports')
    generated_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=500, blank=True)
    summary_data = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()}"
    
    class Meta:
        ordering = ['-generated_at']


class AcademicGoal(models.Model):
    """
    Student academic goals and targets
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='academic_goals')
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    target_semester = models.PositiveIntegerField()
    target_year = models.CharField(max_length=10)
    is_achieved = models.BooleanField(default=False)
    achieved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']
