from django.contrib import admin

from .models import Question, Choice, Quiz


# admin.site.register(Choice)

admin.site.site_header = "Pollster Admin"
admin.site.site_title = "Pollster Admin Area"
admin.site.index_title = "Welcome to the Pollster Admin Area"


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3
    max_num = 3
    can_delete = False

class QuestionInLine(admin.StackedInline):
    model = Question
    extra = 0
    exclude = ('question_text',)
    show_change_link = True



class QuizAdmin(admin.ModelAdmin):
    model = Quiz

    list_display = ('quiz_title', 'description' )
    fields = ('quiz_title', 'description' )
    inlines = [QuestionInLine]

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    fieldsets = [(None, {'fields': ['question_text']}), ('Date Information', {
        'fields': [], 'classes': ['collapse']}), ]
    inlines = [ChoiceInLine]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
