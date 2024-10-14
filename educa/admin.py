from django.contrib import admin

from .models import *

@admin.register(Direction)
class AdminDirection(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Project)
class AdminProject(admin.ModelAdmin):
    list_display = ('id','name','get_direction','get_director','task')

@admin.register(InternShip)
class AdminInternShip(admin.ModelAdmin):
    list_display = ('id','name','get_direction','get_director','get_courses','get_interns')

@admin.register(Kata)
class AdminKata(admin.ModelAdmin):
    list_display = ('id','name','get_owner','base','solution')

@admin.register(Test)
class AdminTest(admin.ModelAdmin):
    list_display = ('id','name','get_owner','base','solution')

@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    list_display = ('id','name','get_owner','type','get_internship','get_interns')

@admin.register(Theme)
class AdminTheme(admin.ModelAdmin):
    list_display = ('id','name','get_owner','get_course','get_kata','get_test','get_interns')

@admin.register(Report)
class AdminReport(admin.ModelAdmin):
    list_display = ('id','name','internshiper','project','date_created','description')