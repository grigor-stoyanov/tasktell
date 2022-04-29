from django.contrib import admin

from tasktell.main.models import Project, Member


class MembersInlineAdmin(admin.TabularInline):
    model = Member.projects.through
    extra = 0


@admin.register(Project)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)
    inlines = (MembersInlineAdmin,)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
