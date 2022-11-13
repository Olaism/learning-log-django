from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model

User = get_user_model()

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=6, unique=True)
    detail = models.TextField(blank=True, default='')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    slug = models.SlugField(blank=True, null=True, max_length=6)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subject_detail', args=(self.slug,))

@receiver(pre_save, sender=Subject)
def subject_slug_handler(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.code)

class Topic(models.Model):
    topic = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

class Entry(models.Model):
    """ Something specific about a topic """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="entries")
    text = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.text[:50] + '...'
