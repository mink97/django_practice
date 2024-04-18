from rest_framework import permissions

class CustomReadonly(permissions.BasePermission):
    # 글 조회 : 모든 사용자 / 글 생성 : 로그인한 사용자 / 글 수정, 삭제 : 글 작성자
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        # return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user