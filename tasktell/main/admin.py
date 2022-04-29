from django.contrib import admin

from tasktell.main.models import Project, Member


class MembersInlineAdmin(admin.StackedInline):
    model = Member


@admin.register(Project)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)
    inlines = (Member,)


@admin.register(Member)
class PetAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
