from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
class Item(models.Model):
    choices = (
        ('Good', 'Good'),
        ('Second', 'Second'),
        ('Bad', 'Bad'),
    )
    name = models.CharField(max_length=150)
    function = models.CharField(max_length=500)
    condition = models.CharField(max_length=100, choices=choices)
    stock = models.PositiveIntegerField()
    division = models.ForeignKey('user.division', on_delete=models.CASCADE, related_name='items')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

