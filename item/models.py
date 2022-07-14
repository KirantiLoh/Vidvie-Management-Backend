from django.db import models
from simple_history.models import HistoricalRecords
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from cloudinary import uploader

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
    borrowed = models.PositiveIntegerField(default=0)
    broken = models.PositiveIntegerField(default=0)
    division = models.ForeignKey('user.division', on_delete=models.CASCADE, related_name='items')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = CloudinaryField('image', null=True, blank=True, folder="items", overwrite=True, invalidate=True, resource_type='image')
    history = HistoricalRecords()

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['condition'])
        ]

    def __str__(self):
        return self.name

@receiver(pre_delete, sender=Item)
def delete_image(sender, instance, **kwargs):
    uploader.destroy(instance.image.public_id, invalidate=True)

