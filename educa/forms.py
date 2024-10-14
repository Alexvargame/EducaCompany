from django import forms
from django.forms import fields,widgets
from django.forms.models import inlineformset_factory
from django.forms import formset_factory, modelformset_factory

from .models import *
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):

    class Meta:
        model=Project
        fields=('name','direction','director','task')
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'empty_value':True}),
            'direction':forms.SelectMultiple(attrs={'class':'form-control', 'empty_value':True},choices=[(dirs.id,dirs.name) for dirs in Direction.objects.all()]),
            'director':forms.SelectMultiple(attrs={'class':'form-control', 'empty_value':True},choices=[(us.id,us.username) for us in User.objects.all()]),
            'task':forms.TextInput(attrs={'class':'form-control', 'empty_value':True})
        }
class InternShipForm(forms.ModelForm):

    class Meta:
        model=InternShip
        fields=('name','direction','director')
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'empty_value':True}),
            'direction':forms.SelectMultiple(attrs={'class':'form-control', 'empty_value':True},choices=[(dirs.id,dirs.name) for dirs in Direction.objects.all()]),
            'director':forms.SelectMultiple(attrs={'class':'form-control', 'empty_value':True},choices=[(us.id,us.username) for us in User.objects.all()]),
        }
class InternShipUpdateForm(forms.Form):

    direction_to_del=forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    direction_to_add=forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    director_to_del=forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    director_to_add=forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    course_to_del = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    course_to_add = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))

class CourseAddForm(forms.Form):
    courses=forms.CharField(widget=forms.CheckboxSelectMultiple(
                                  choices=sorted([(obj.id, obj.name) for obj in Course.objects.all()])))

class CourseForm(forms.ModelForm):

    class Meta:
        model=Course
        fields=('name','owner','internship','type')
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'empty_value':True}),
            'internship':forms.SelectMultiple(attrs={'class':'form-control', 'empty_value':True},choices=[(intern.id,intern.name) for intern in InternShip.objects.all()]),
            'owner':forms.SelectMultiple(attrs={'class':'form-control', 'empty_value':True},choices=[(us.id,us.username) for us in User.objects.all()]),
            'type':forms.Select(attrs={'class':'form-control', 'empty_value':True},choices=[('theory','theory'),('practic','practic')])
        }
class CourseUpdateForm(forms.Form):

    owner_to_del=forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    owner_to_add=forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    theme_to_del = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    theme_to_add = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))

class ThemeAddForm(forms.Form):
    themes=forms.CharField(widget=forms.CheckboxSelectMultiple(
                                  choices=sorted([(obj.id, obj.name) for obj in Theme.objects.all()])))
class ThemeForm(forms.ModelForm):

    class Meta:
        model=Theme
        fields=('name','owner','course','test','kata')
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'empty_value':True}),
            'course':forms.SelectMultiple(attrs={'class':'form-control', 'empty_value':True},choices=[(course.id,course.name) for course in Course.objects.all()]),
            'owner':forms.SelectMultiple(attrs={'class':'form-control', 'empty_value':True},choices=[(us.id,us.username) for us in User.objects.all()]),
            'test':forms.CheckboxSelectMultiple(
                                  choices=sorted([(obj.id, obj.name) for obj in Test.objects.all()])),
            'kata':forms.CheckboxSelectMultiple(
                                    choices=sorted([(obj.id, obj.name) for obj in Kata.objects.all()]))
        }
class ThemeUpdateForm(forms.Form):
    owner_to_del=forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    owner_to_add=forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    test_to_del = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    test_to_add = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    kata_to_del = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[], attrs={'empty_value': True}))
    kata_to_add = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[], attrs={'empty_value': True}))
class TestForm(forms.ModelForm):
    class Meta:
        model=Test
        fields=('name','owner','base')
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'empty_value':True}),
            'base':forms.TextInput(attrs={'class':'form-control', 'empty_value':True}),
            'owner':forms.SelectMultiple(attrs={'class':'form-control', 'empty_value':True},choices=[(us.id,us.username) for us in User.objects.all()]),
        }
class KataForm(forms.ModelForm):
    class Meta:
        model=Kata
        fields=('name','owner','base')
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'empty_value':True}),
            'base':forms.TextInput(attrs={'class':'form-control', 'empty_value':True}),
            'owner':forms.SelectMultiple(attrs={'class':'form-control', 'empty_value':True},choices=[(us.id,us.username) for us in User.objects.all()]),
        }
class OwnerUpdateForm(forms.Form):
    owner_to_del=forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))
    owner_to_add=forms.CharField(widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))

class InternShipEnrollForm(forms.Form):
    internships = forms.IntegerField(widget=forms.HiddenInput)


class CourseEnrollForm(forms.Form):
    courses = forms.IntegerField(widget=forms.HiddenInput)

class ThemeEnrollForm(forms.Form):
    themes = forms.IntegerField(widget=forms.HiddenInput)

class KataAnswerForm(forms.Form):
    answer=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'empty_value':True}))

class TestAnswerForm(forms.Form):
    answer=forms.JSONField(widget=forms.Textarea(attrs={'class':'form-control', 'empty_value':True}))

class UnEnrollCourseForm(forms.Form):
    courses=forms.CharField(required=False,widget=forms.CheckboxSelectMultiple(choices=[],attrs={'empty_value':True}))

class ProjectEnrollForm(forms.Form):
    projects = forms.IntegerField(widget=forms.HiddenInput)

class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model=Report
        fields=('edit_field',)
        widgets={
            'edit_field':forms.Textarea(attrs={'class':'form-control', 'empty_value':True})
        }
# CourseEnrollFormSet=modelformset_factory(Course,fields=('name','type'))
# CourseEnrollFormSet1=formset_factory(CourseAddForm)
# ThemeEnrollFormSet=modelformset_factory(Theme,fields=('name',))
#     #inlineformset_factory(InternShip,Course,fields=['name','type'],extra=2,can_delete=True)