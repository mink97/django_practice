from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):
    # GET = 누구나, PUT/PATCH = 해당 유저만
    def has_object_permission(self, request, view, obj): # obj = 해당 객체
        if request.method in permissions.SAFE_METHODS: # SAFE_METHODS = GET, HEAD, OPTIONS(데이터에 영향 x)
            return True
        return obj.user == request.user