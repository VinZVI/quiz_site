from django.contrib import admin

from .models import Question, Choice, Quiz


# admin.site.register(Choice)

admin.site.site_header = "Quizzes Admin"
admin.site.site_title = "Quizzes Admin Area"
admin.site.index_title = "Welcome to the Quizzes Admin Area"


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3
    max_num = 3
    can_delete = False

class QuestionInLine(admin.StackedInline):
    model = Question
    extra = 0
    exclude = ('slug',)
    show_change_link = True



class QuizAdmin(admin.ModelAdmin):
    model = Quiz
    list_display = ['quiz_title', 'slug', 'author', 'publish', 'status' ]
    list_filter = ['status', 'publish', 'author']
    search_fields = ['quiz_title', 'description']
    prepopulated_fields = {'slug': ('quiz_title',)}
    raw_id_fields = ['author'] # поиск по id
    date_hierarchy = 'publish' # иерархия по дате
    ordering = ['status', 'publish']
    fields = ['quiz_title', 'slug', ('author', 'status'),'description']
    inlines = [QuestionInLine]

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ['question_text', 'slug', 'quiz']
    list_filter = ['quiz']
    search_fields = ['question_text', 'quiz']
    prepopulated_fields = {'slug': ('question_text',)} # предварительно заполнить slug поле с вводом title поле
    #raw_id_fields = ['quiz']
    #date_hierarchy = 'quiz'
    ordering = ['quiz']
    fields = ('question_text', 'slug', 'quiz')
    # fieldsets = [(None, {'fields': ['question_text']}), ('Date Information', {
    #     'fields': [], 'classes': ['collapse']}), ]
    inlines = [ChoiceInLine]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
