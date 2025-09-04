from django.db import models
from accounts.models import User


class KnowledgeBase(models.Model):
    """
    Knowledge base articles and FAQs
    """
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('administrative', 'Administrative'),
        ('technical', 'Technical'),
        ('general', 'General'),
        ('policy', 'Policy'),
        ('procedure', 'Procedure'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    content = models.TextField()
    keywords = models.TextField(help_text="Comma-separated keywords for search")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_knowledge_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"
    
    class Meta:
        ordering = ['-created_at']


class ChatSession(models.Model):
    """
    Chat sessions with the AI assistant
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id = models.CharField(max_length=100, unique=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    context = models.JSONField(default=dict, help_text="Session context and metadata")
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.session_id}"
    
    class Meta:
        ordering = ['-last_activity']


class ChatMessage(models.Model):
    """
    Individual chat messages
    """
    MESSAGE_TYPE_CHOICES = [
        ('user', 'User Message'),
        ('assistant', 'Assistant Response'),
        ('system', 'System Message'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, help_text="Additional message metadata")
    
    def __str__(self):
        return f"{self.session.user.get_full_name()} - {self.get_message_type_display()} - {self.timestamp}"
    
    class Meta:
        ordering = ['timestamp']


class AIResponse(models.Model):
    """
    AI-generated responses for tracking and improvement
    """
    query = models.TextField()
    response = models.TextField()
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    knowledge_sources = models.JSONField(default=list, help_text="Sources used for the response")
    user_feedback = models.CharField(max_length=20, blank=True, choices=[
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('incorrect', 'Incorrect'),
    ])
    feedback_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Query: {self.query[:50]}... - Score: {self.confidence_score}"
    
    class Meta:
        ordering = ['-created_at']


class FAQ(models.Model):
    """
    Frequently Asked Questions
    """
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=50)
    tags = models.TextField(help_text="Comma-separated tags")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.question[:50]}..."
    
    class Meta:
        ordering = ['-view_count']


class SupportTicket(models.Model):
    """
    Support tickets for complex queries
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tickets', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"#{self.id} - {self.subject} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']


class TicketResponse(models.Model):
    """
    Responses to support tickets
    """
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_responses')
    response = models.TextField()
    is_internal = models.BooleanField(default=False, help_text="Internal note not visible to user")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to #{self.ticket.id} by {self.responder.get_full_name()}"
    
    class Meta:
        ordering = ['created_at']


class AIConfiguration(models.Model):
    """
    Configuration for AI assistant behavior
    """
    name = models.CharField(max_length=100, unique=True)
    model_name = models.CharField(max_length=100, default='gemini-pro')
    temperature = models.DecimalField(max_digits=3, decimal_places=2, default=0.7)
    max_tokens = models.PositiveIntegerField(default=1000)
    system_prompt = models.TextField(help_text="System prompt for AI behavior")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.model_name}"
    
    class Meta:
        ordering = ['-updated_at']


class ConversationAnalytics(models.Model):
    """
    Analytics for conversation patterns and improvements
    """
    date = models.DateField()
    total_conversations = models.PositiveIntegerField(default=0)
    total_messages = models.PositiveIntegerField(default=0)
    avg_messages_per_conversation = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    user_satisfaction_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    common_queries = models.JSONField(default=list, help_text="Most common user queries")
    resolution_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analytics for {self.date} - {self.total_conversations} conversations"
    
    class Meta:
        unique_together = ['date']
        verbose_name_plural = 'Conversation Analytics'
        ordering = ['-date']
