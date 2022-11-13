from django.contrib import admin

from .models import (
    Subject,
    Topic,
    Entry
)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    list_display = ('name', 'code', 'date_added')
    prepopulated_fields = {
        'slug': ('code',)
    }

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    model = Topic
    list_display = ('topic', 'id', 'subject', 'date_added')

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    model = Entry
    list_display = ('topic', 'text', 'id', 'date_added')