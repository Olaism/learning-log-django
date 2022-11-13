from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView
)

from .models import (
    Subject,
    Topic,
    Entry
)

from .forms import (
    SubjectForm,
    TopicForm,
    EntryForm
)

class SubjectList(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'logs/subjects.html'
    context_object_name = 'subjects'
    ordering = ['-date_added']
    
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            q_subjects = queryset.filter(name__icontains=query)\
            .filter(owner=self.request.user)
            return q_subjects
        new_queryset = queryset.filter(owner=self.request.user)
        return new_queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['section'] = 'subject-list'
        return context

class SubjectDetail(LoginRequiredMixin, DetailView):
    model = Subject
    template_name = 'logs/subject.html'
    context_object_name = 'subject'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['section'] = 'subject-detail'
        return context

class SubjectSearch(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'logs/subjects.html'
    context_object_name = 'subjects'
    ordering = ['-date_added']

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        query = self.kwargs.get('term')
        if query:
            return queryset.filter(name__icontains=query).filter(owner=self.request.user)
        return []

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['section'] = 'subject-search'
        return context

@login_required
def new_subject(request):
    """ Add a new subject """
    if request.method == 'POST':
        #No data submitted, create a blank form
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.owner = request.user
            subject.save()
            return redirect('logs:subject_list')
    else:
        # POST data submitted, process data
        form = SubjectForm()

    return render(request, 'logs/new_subject.html', {'form': form})

@login_required
def delete_subject(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    if subject.owner != request.user:
        raise Http404
    else:
        subject.delete()
    return redirect('logs:subject_list')

@login_required
def topic_detail(request, subject_slug, pk):
    topic = get_object_or_404(Topic, subject__slug=subject_slug, pk=pk)
    if topic.subject.owner != request.user:
        raise Http404
    return render(request, 'logs/topic.html', {'topic': topic, 'section': 'topic-detail'})

@login_required
def new_topic(request, subject_slug):
    """ Add a new topic """
    subject = get_object_or_404(Subject, slug=subject_slug)
    if subject.owner != request.user:
        raise Http404
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.subject = subject
            topic.save()
            return redirect('logs:topic_detail', subject.slug, topic.pk)
    else:
        form = TopicForm()

    return render(request, 'logs/new_topic.html', {'form': form})

@login_required
def edit_topic(request, subject_slug, pk):
    """ Edit existing topic """
    topic = get_object_or_404(Topic, subject__slug=subject_slug, pk=pk)
    if topic.subject.owner != request.user:
        raise Http404
    if request.method == 'POST':
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logs:topic_detail', topic.subject.slug, topic.pk)
    else:
        form = TopicForm(instance=topic)

    return render(request, 'logs/new_topic.html', {'form': form})

@login_required
def delete_topic(request, subject_slug, pk):
    """ delete existing topic """
    topic = get_object_or_404(Topic, subject__slug=subject_slug, pk=pk)
    if topic.subject.owner != request.user:
        raise Http404
    topic.delete()
    return redirect('logs:subject_detail', topic.subject.slug)

@login_required
def new_entry(request, subject_slug, topic_pk):
    """ Add a new entry """
    topic = get_object_or_404(Topic, subject__slug=subject_slug, pk=topic_pk)
    if topic.subject.owner != request.user:
        raise Http404
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('logs:topic_detail', topic.subject.slug, topic.pk)
    else:
        form = EntryForm()

    return render(request, 'logs/new_entry.html', {'form': form})

@login_required
def edit_entry(request, subject_slug, topic_pk, pk):
    """ Edit existing entry """
    entry = get_object_or_404(Entry, topic__subject__slug=subject_slug, topic__pk=topic_pk, pk=pk)
    if entry.topic.subject.owner != request.user:
        raise Http404
    if request.method == 'POST':
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logs:topic_detail', entry.topic.subject.slug, entry.topic.pk)
    else:
        form = EntryForm(instance=entry)

    return render(request, 'logs/new_entry.html', {'form': form})

@login_required
def delete_entry(request, subject_slug, topic_pk, pk):
    """ Delete existing entry """
    entry = get_object_or_404(Entry, topic__subject__slug=subject_slug, topic__pk=topic_pk, pk=pk)
    if entry.topic.subject.owner != request.user:
        raise Http404
    entry.delete()
    return redirect('logs:topic_detail', entry.topic.subject.slug, entry.topic.pk)