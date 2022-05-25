from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=100)
    leader = models.OneToOneField('user.account', on_delete=models.CASCADE, related_name='leader_of', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=20, default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.leader:
            self.leader.division = self
            self.leader.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Account(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='members', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

'''
 (
        ('OM', 'Online Marketing'),
        ('BR', 'Branding'),
        ('SLS', 'Sales'),
        ('HRD', 'HRD'),
        ('GA', 'GA'),
        ('OP', 'Operantional'),
        ('ST', 'Store'),
        ('', 'Vidvie'),
        ('', 'Direksi'),
        ('DIS', 'Distributor'),
        ('OTH', 'Others')
    )
 '''   


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        try:
            other_division = Division.objects.get(name='Others')
            account = Account.objects.create(user=instance, division=other_division)
        except ObjectDoesNotExist:
            account = Account.objects.create(user=instance)
        finally:
            account.save()
