from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    priority_choices = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    )
    status_choices = (
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Shipping', 'Shipping'),
        ('Finished', 'Finished'),
    )
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    priority = models.CharField(max_length=10, choices=priority_choices)
    status = models.CharField(max_length=20, choices=status_choices)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    requestor_division = models.ForeignKey('user.division', on_delete=models.CASCADE, related_name='requests')
    requestee_division = models.ForeignKey('user.division', on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ('-date_added','-id')