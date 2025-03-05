from rest_framework import permissions


class CreateEmployeePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('users.add_user')


class CreateCompanyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm("users.add_company")
