from pydoc import describe
from django.db import models

# Create your models here.
class HandOver(models.Model):
    requestor_division = models.ForeignKey('user.division', on_delete= models.PROTECT, related_name='requestor_division')
    requestor = models.ForeignKey('user.account', on_delete= models.PROTECT, related_name='requestor')
    requestee_division = models.ForeignKey('user.division', on_delete= models.PROTECT, related_name='requestee_division')
    item = models.ForeignKey('item.item', on_delete= models.PROTECT)
    count = models.PositiveIntegerField()
    description = models.TextField()
    is_approved = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name}"