from rest_framework import permissions

class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(obj)
        return obj.owner == request.user
        # or obj.subject.owner == request.user
        # or obj.topic.subject.owner == request.user