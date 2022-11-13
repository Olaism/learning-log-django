from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    subject_list,
    subject_detail,
    topic_create,
    TopicDetail,
    entry_create,
    EntryDetail,
)

app_name = 'api'

urlpatterns = [
    path('logs/', subject_list),
    path('logs/<slug:slug>/', subject_detail),
    path('logs/<slug:subject_slug>/topic/new/', topic_create),
    path('logs/<slug:subject_slug>/topic/<int:pk>/', TopicDetail.as_view()),
    path('logs/<slug:subject_slug>/topic/<int:topic_pk>/entry/new/', entry_create),
    path('logs/<slug:subject_slug>/topic/<int:topic_pk>/entry/<pk>/', EntryDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)