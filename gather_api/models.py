# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import random
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
import social_django



class User(AbstractUser):
    social_id = models.IntegerField(blank=True, null=True)
    profile_pic = models.CharField(blank=True, null=True, max_length=300)

    class Meta:
        ordering = ['id']




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

    class Meta:
        ordering = ['created']

# Create your models here.
class Node(models.Model):
    owner = models.ForeignKey('User', related_name='node', on_delete=models.CASCADE)
    minor = models.IntegerField(blank=True)
    major = models.IntegerField(blank=True)
    uuid = models.UUIDField()
    device_name = models.CharField(max_length=32)
    device_token = models.CharField(blank=True, null=True, max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    userid = models.IntegerField(null=True)


    def save(self, *args, **kwargs):
        self.minor = random.randint(0,100)
        self.major = random.randint(0,100)
        self.userid = self.owner.id
        super(Node, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created']


class Connection(models.Model):
    source = models.ForeignKey('Node', on_delete=models.CASCADE, related_name="source-connection+")
    destination = models.ForeignKey('Node', on_delete=models.CASCADE, related_name="dest-connection+")
    waved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['updated']


class Message(models.Model):
     sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sender')
     receiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='receiver')
     message = models.CharField(max_length=1200)
     timestamp = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default=False)
     def __str__(self):
           return self.message
     class Meta:
           ordering = ('timestamp',)
