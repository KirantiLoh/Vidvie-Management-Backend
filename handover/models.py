from django.forms import ValidationError
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.
class HandOver(models.Model):
    tipe_form = (
        ('Peminjaman', 'Peminjaman'),
        ('Pengembalian', 'Pengembalian'),
        ('Permintaan', 'Permintaan'),
        )
    tipe = models.CharField(max_length=50, choices=tipe_form)
    requestor_division = models.ForeignKey('user.division', on_delete= models.PROTECT, related_name='requestor_division')
    requestor = models.ForeignKey('user.account', on_delete= models.PROTECT, related_name='requestor')
    requestee_division = models.ForeignKey('user.division', on_delete= models.PROTECT, related_name='requestee_division')
    item = models.ForeignKey('item.item', on_delete= models.PROTECT)
    count = models.PositiveIntegerField(default=1)
    description = models.TextField()
    is_approved = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def clean(self):
        if self.requestor.division != self.requestor_division:
            raise ValidationError('The requesting user is not from the inputed requesting division')
        if self.item.division != self.requestee_division:
            raise ValidationError('The requested item is not from the inputed requested division')
        if self.requestor_division == self.requestee_division:
            raise ValidationError('You cannot borrow items from your own division')
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name}"


@receiver(pre_save, sender = HandOver)
def update_item_stock(sender, instance, *args, **kwargs):
    item = instance.item
    if (instance.tipe == 'Peminjaman'): 
        item.stock -= instance.count
        item.borrowed += instance.count
    elif(instance.tipe == 'Permintaan'):
        item.stock -= instance.count
    else:
        item.stock += instance.count
        item.borrowed -= instance.count
    item.save()