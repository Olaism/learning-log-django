from django.urls import path

from .views import (
    SubjectList,
    SubjectDetail,
    SubjectSearch,
    delete_subject,
    topic_detail,
    new_subject,
    new_topic,
    edit_topic,
    delete_topic,
    new_entry,
    edit_entry,
    delete_entry,
)

app_name = 'logs'

urlpatterns = [
    path('', SubjectList.as_view(), name='subject_list'),
    path('new/', new_subject, name='new_subject'),
    path('<slug:slug>/delete/', delete_subject, name='delete_subject'),
    path('search/<str:term>/', SubjectSearch.as_view(), name='subject_search'),
    path('<slug:subject_slug>/topic/new/', new_topic, name='new_topic'),
    path('<slug:subject_slug>/topic/<int:pk>/edit/', edit_topic, name='edit_topic'),
    path('<slug:subject_slug>/topic/<int:pk>/delete/', delete_topic, name='delete_topic'),
    path('<slug:subject_slug>/topic/<int:topic_pk>/entry/new/', new_entry, name='new_entry'),
    path('<slug:subject_slug>/topic/<int:topic_pk>/entry/<int:pk>/edit/', edit_entry, name='edit_entry'),
    path('<slug:subject_slug>/topic/<int:topic_pk>/entry/<int:pk>/delete/', delete_entry, name='delete_entry'),
    path('<slug:slug>/', SubjectDetail.as_view(), name='subject_detail'),
    path('<slug:subject_slug>/topic/<int:pk>/', topic_detail, name='topic_detail'),
]