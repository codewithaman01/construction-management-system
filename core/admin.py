from django.contrib import admin
from .models import Module, RolePermission


# 🔥 MODULE ADMIN
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_default')
    list_editable = ('is_default',)
    search_fields = ('name', 'url')
    list_filter = ('is_default',)
    ordering = ('name',)

    # 👉 detailed form view
    fieldsets = (
        ('Module Info', {
            'fields': ('name', 'url')
        }),
        ('Settings', {
            'fields': ('is_default',)
        }),
    )


# 🔥 ROLE PERMISSION ADMIN
@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'module')
    list_filter = ('role', 'module')
    search_fields = ('role__name', 'module__name')

    # 👉 dropdown improves UI
    autocomplete_fields = ['role', 'module']

    # 👉 form layout
    fieldsets = (
        ('Permission Setup', {
            'fields': ('role', 'module')
        }),
    )