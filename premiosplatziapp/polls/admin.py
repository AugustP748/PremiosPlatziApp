from django.contrib import admin
from .models import Question,Choice

# Register your models here.

class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "questionText"]
    inlines = [ChoiceInLine]
    list_display = ("questionText", "pub_date","was_published_recently" )
    list_filter = ["pub_date"]
    search_fields = ["questionText"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)