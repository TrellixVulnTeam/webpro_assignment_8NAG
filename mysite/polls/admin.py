from django.contrib import admin
from django.contrib.auth.models import Permission

# Register your models here.
from polls.models import Poll, Question, Choice, Comment

admin.site.register(Permission)

class QuestionInline(admin.StackedInline):
    model = Question

class PollAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start_date', 'end_date', 'del_flag']
    list_per_page = 10

    list_filter = ['start_date', 'end_date', 'del_flag', 'title']
    search_fields = ['title']

    # fields เลือกแสดง field ที่เลือก
    # fields = ['title', 'del_flag']

    # exclude เลือกเอา field ที่เลือกออก
    # exclude = ['title']

    fieldsets = [
        (None, {'fields': ['title', 'del_flag']}),
        ("Active Duration", {'fields': ['start_date', 'end_date'], 'classes': ['collapse']})
    ]

    inlines = [QuestionInline]

admin.site.register(Poll, PollAdmin)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'poll', 'text']
    list_per_page = 15

    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'text', 'value']
    list_per_page = 15

admin.site.register(Choice, ChoiceAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'email', 'tel', 'poll']
    list_filter = ['poll']
    search_fields = ['title']

admin.site.register(Comment, CommentAdmin)
