from django import forms
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.cache import cache

from datetime import datetime

import json
from .utils import TypeCourseListMixin,TypeCourseDetailMixin,TypeCourseDeleteMixin,TrainMixin
from .models import Project,InternShip,Course,Theme,Test,Kata,Direction,Report

from .forms import (ProjectForm,InternShipForm,CourseAddForm,CourseForm,
                    ThemeAddForm,ThemeForm, TestForm,KataForm,
                    InternShipUpdateForm,CourseUpdateForm,ThemeUpdateForm,
                    OwnerUpdateForm,InternShipEnrollForm,CourseEnrollForm,
                    ThemeEnrollForm,KataAnswerForm,TestAnswerForm,
                    UnEnrollCourseForm,ProjectEnrollForm,ReportUpdateForm)


def main_page(request):
    return render(request,'educa/main_page.html')


class ProjectsListView(LoginRequiredMixin,TypeCourseListMixin,View):
    model=Project
    templates='educa/projects_list.html'



class ProjectDetailView(LoginRequiredMixin,TypeCourseDetailMixin,View):
    model=Project
    templates='educa/project_detail.html'
    form = ProjectEnrollForm

class ProjectCreateView(LoginRequiredMixin,View):

    def get(self,request):
        form=ProjectForm()
        return render(request,'educa/project_create.html',{'form':form})

    def post(self,request):
        bound_form=ProjectForm(request.POST)
        if bound_form.is_valid():
            new_proj=bound_form.save()
            return redirect(new_proj)
        return render(request,'educa/project_create.html',{'form':bound_form})

class ProjectDeleteView(LoginRequiredMixin,TypeCourseDeleteMixin,View):
    model = Project
    url = 'projects_list_url'
    templates='educa/project_delete.html'

class InternShipsListView(LoginRequiredMixin,TypeCourseListMixin,View):
    model=InternShip
    templates='educa/internships_list.html'


class InternShipDetailView(LoginRequiredMixin,TypeCourseDetailMixin,View):
    model = InternShip
    templates = 'educa/internship_detail.html'
    form=InternShipEnrollForm

class InternShipCreateView(LoginRequiredMixin,View):

    def get(self,request):
        form=InternShipForm()
        form_course=CourseAddForm()

        return render(request,'educa/internship_create.html',{'form':form,'form_course':form_course})

    def post(self,request):
        bound_form=InternShipForm(request.POST)
        bound_form_course=CourseAddForm(request.POST)
        if bound_form.is_valid() and bound_form_course.is_valid():
            new_intern=bound_form.save()
            new_intern.courses.add(*bound_form_course['courses'].value())
            new_intern.save()
            return redirect(new_intern)
        return render(request,'educa/internship_create.html',{'form':bound_form,'form_course':bound_form_course})

class InternShipUpdateView(LoginRequiredMixin,View):

    def get(self,request,pk):
        internship=InternShip.objects.get(id=pk)
        form=InternShipForm(instance=internship)
        form_2=InternShipUpdateForm()

        context = {'form': form,
                   'internship':internship,
                   'direction_to_del':form_2['direction_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(dirs.id,dirs.name) for dirs in internship.get_direction()])),
                   'direction_to_add': form_2['direction_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(dirs.id, dirs.name) for dirs in Direction.objects.all() if dirs not in internship.get_direction()])),
                   'director_to_del': form_2['director_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(direct.id, direct.username) for direct in internship.get_director()])),
                   'directior_to_add': form_2['director_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(direct.id, direct.username) for direct in User.objects.all() if
                                direct not in internship.get_director()])),
                   'course_to_del': form_2['course_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(course.id, course.name) for course in internship.get_courses()])),
                   'course_to_add': form_2['course_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(course.id, course.name) for course in Course.objects.all() if
                                course not in internship.get_courses()])),
                   }

        return render(request,'educa/internship_update.html',context=context)

    def post(self,request,pk):
        internship = InternShip.objects.get(id=pk)
        bound_form = InternShipForm(request.POST,instance=internship)
        bound_form_2=InternShipUpdateForm(request.POST)
        context = {'form': bound_form,
                   'internship': internship,
                   'direction_to_del': bound_form_2['direction_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(dirs.id, dirs.name) for dirs in internship.get_direction()])),
                   'direction_to_add': bound_form_2['direction_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(dirs.id, dirs.name) for dirs in Direction.objects.all() if
                                dirs not in internship.get_direction()])),
                   'director_to_del': bound_form_2['director_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(direct.id, direct.username) for direct in internship.get_director()])),
                   'director_to_add': bound_form_2['director_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(direct.id, direct.username) for direct in User.objects.all() if
                                direct not in internship.get_director()])),
                   'course_to_del': bound_form_2['course_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(course.id, course.name) for course in internship.get_courses()])),
                   'course_to_add': bound_form_2['course_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(course.id, course.name) for course in Course.objects.all() if
                                course not in internship.get_courses()])),
                   }
        new_direction=[dirs.id for dirs in internship.get_direction() if str(dirs.id) not in bound_form_2['direction_to_del'].value()]
        new_direction.extend([dirs.id for dirs in Direction.objects.filter(id__in=bound_form_2['direction_to_add'].value())])
        new_director = [direct.id for direct in internship.get_director() if
                         str(direct.id) not in bound_form_2['director_to_del'].value()]
        new_director.extend([direct.id for direct in User.objects.filter(id__in=bound_form_2['director_to_add'].value())])
        new_course = [course.id for course in internship.get_courses() if
                        str(course.id) not in bound_form_2['course_to_del'].value()]
        new_course.extend([course.id for course in Course.objects.filter(id__in=bound_form_2['course_to_add'].value())])
        if bound_form.is_valid():
            new_intern=bound_form.save()
            new_intern.direction.set(new_direction)
            new_intern.director.set(new_director)
            new_intern.courses.set(new_course)
            new_intern.save()
            # for intern in new_intern.interns.all():
            #     for course in new_intern.get_courses():
            #         if intern in course.get_interns():
            #             for key, value in intern.profile.assesments.items():
            #                 print(key,value)
            #                 for k, v in intern.profile.assesments[key].items():
            #                     print(k,v)
            #                     if k == course.name:
            #                         for theme in course.get_themes():
            #                             if theme not in intern.profile.assesments[key][k].keys():
            #                                 intern.profile.assesments[key][k][str(theme)] = {}
            #                             for test in theme.get_test():
            #                                 intern.profile.assesments[key][k][str(theme)][str(test)] = 0
            #                             for kata in theme.get_kata():
            #                                 intern.profile.assesments[key][k][str(theme)][str(kata)] = 0
            #                             intern.profile.save()
            return redirect(new_intern)
        return render(request,'educa/internship_update.html',{'form':bound_form})

class InternShipDeleteView(LoginRequiredMixin,TypeCourseDeleteMixin,View):
    model = InternShip
    url = 'internships_list_url'
    templates='educa/internship_delete.html'

class CoursesListView(LoginRequiredMixin,TypeCourseListMixin,View):
    model=Course
    templates='educa/courses_list.html'


class CourseDetailView(LoginRequiredMixin,TypeCourseDetailMixin,View):
    model = Course
    templates = 'educa/course_detail.html'
    form=CourseEnrollForm

class CourseCreateView(LoginRequiredMixin,View):

    def get(self,request):
        form=CourseForm()
        form_theme=ThemeAddForm()
        return render(request,'educa/course_create.html',{'form':form,'form_theme':form_theme})

    def post(self,request):
        bound_form=CourseForm(request.POST)
        bound_form_theme=ThemeAddForm(request.POST)
        if bound_form.is_valid():
            new_course=bound_form.save()
            new_course.course_themes.add(*bound_form_theme['themes'].value())
            new_course.save()
            return redirect(new_course)
        return render(request,'educa/course_create.html',{'form':bound_form,'form_theme':bound_form_theme})

class CourseUpdateView(LoginRequiredMixin,View):

    def get(self,request,pk):
        course=Course.objects.get(id=pk)
        form=CourseForm(instance=course)
        form_2=CourseUpdateForm()

        context = {'form': form,
                   'course':course,
                   'owner_to_del': form_2['owner_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in course.get_owner()])),
                   'owner_to_add': form_2['owner_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in User.objects.all() if
                                own not in course.get_owner()])),
                   'theme_to_del': form_2['theme_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(theme.id, theme.name) for theme in course.get_themes()])),
                   'theme_to_add': form_2['theme_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(theme.id, theme.name) for theme in Theme.objects.all() if
                                theme not in course.get_themes()])),
                   }
        return render(request,'educa/course_update.html',context=context)

    def post(self,request,pk):
        course = Course.objects.get(id=pk)
        bound_form = CourseForm(request.POST,instance=course)
        bound_form_2=CourseUpdateForm(request.POST)
        context = { 'form': bound_form,
                    'course': course,
                    'owner_to_del': bound_form_2['owner_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in course.get_owner()])),
                    'owner_to_add': bound_form_2['owner_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in User.objects.all() if
                                own not in course.get_owner()])),
                    'theme_to_del': bound_form_2['theme_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(theme.id, theme.name) for theme in course.get_themes()])),
                    'theme_to_add': bound_form_2['theme_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(theme.id, theme.name) for theme in Theme.objects.all() if
                                theme not in course.get_themes()])),
                   }
        new_owner = [own.id for own in course.get_owner() if
                         str(own.id) not in bound_form_2['owner_to_del'].value()]
        new_owner.extend([own.id for own in User.objects.filter(id__in=bound_form_2['owner_to_add'].value())])
        new_theme = [theme.id for theme in course.get_themes() if
                        str(theme.id) not in bound_form_2['theme_to_del'].value()]
        new_theme.extend([theme.id for theme in Theme.objects.filter(id__in=bound_form_2['theme_to_add'].value())])
        if bound_form.is_valid():
            new_course=bound_form.save()
            new_course.owner.set(new_owner)
            new_course.course_themes.set(new_theme)
            new_course.save()
            for intern in new_course.interns.all():
                for key,value in intern.profile.assesments.items():
                    for k,v in intern.profile.assesments[key].items():
                        if k==new_course.name:
                            for theme in new_course.get_themes():
                                if theme not in intern.profile.assesments[key][k].keys():
                                    intern.profile.assesments[key][k][str(theme)]={}
                                for test in theme.get_test():
                                    intern.profile.assesments[key][k][str(theme)][str(test)]=0
                                for kata in theme.get_kata():
                                    intern.profile.assesments[key][k][str(theme)][str(kata)]=0
                                intern.profile.save()
            return redirect(new_course)
        return render(request,'educa/course_update.html',{'form':bound_form})
class CourseDeleteView(LoginRequiredMixin,TypeCourseDeleteMixin,View):
    model = Course
    url = 'courses_list_url'
    templates='educa/course_delete.html'
class ThemesListView(LoginRequiredMixin,TypeCourseListMixin,View):
    model=Theme
    templates='educa/themes_list.html'


class ThemeDetailView(LoginRequiredMixin,TypeCourseDetailMixin,View):
    model = Theme
    templates = 'educa/theme_detail.html'
    form=ThemeEnrollForm
class ThemeCreateView(LoginRequiredMixin,View):

    def get(self,request):
        form=ThemeForm()
        return render(request,'educa/theme_create.html',{'form':form})

    def post(self,request):
        bound_form=ThemeForm(request.POST)
        if bound_form.is_valid():
            new_theme=bound_form.save()
            return redirect(new_theme)
        return render(request,'educa/theme_create.html',{'form':bound_form})

class ThemeUpdateView(LoginRequiredMixin,View):

    def get(self,request,pk):
        theme=Theme.objects.get(id=pk)
        form=ThemeForm(instance=theme)
        form_2=ThemeUpdateForm()
        context = {'form': form,
                   'theme':theme,
                   'owner_to_del': form_2['owner_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in theme.get_owner()])),
                   'owner_to_add': form_2['owner_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in User.objects.all() if
                                own not in theme.get_owner()])),
                   'test_to_del': form_2['test_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(test.id, test.name) for test in theme.get_test()])),
                   'test_to_add': form_2['test_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(test.id, test.name) for test in Test.objects.all() if
                                test not in theme.get_test()])),
                   'kata_to_del': form_2['kata_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(kata.id, kata.name) for kata in theme.get_kata()])),
                   'kata_to_add': form_2['kata_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(kata.id, kata.name) for kata in Kata.objects.all() if
                                kata not in theme.get_kata()])),
                   }
        return render(request,'educa/theme_update.html',context=context)

    def post(self,request,pk):
        theme = Theme.objects.get(id=pk)
        bound_form = ThemeForm(request.POST,instance=theme)
        bound_form_2=ThemeUpdateForm(request.POST)
        context = {'form': bound_form,
                   'theme': theme,
                   'owner_to_del': bound_form_2['owner_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in theme.get_owner()])),
                   'owner_to_add': bound_form_2['owner_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in User.objects.all() if
                                own not in theme.get_owner()])),
                   'test_to_del': bound_form_2['test_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(test.id, test.name) for test in theme.get_test()])),
                   'teste_to_add': bound_form_2['test_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(test.id, test.name) for test in Test.objects.all() if
                                test not in theme.get_test()])),
                   'kata_to_del': bound_form_2['kata_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(kata.id, kata.name) for kata in theme.get_kata()])),
                   'kata_to_add': bound_form_2['kata_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(kata.id, kata.name) for kata in Kata.objects.all() if
                                kata not in theme.get_kata()])),
                   }
        new_owner = [own.id for own in theme.get_owner() if
                         str(own.id) not in bound_form_2['owner_to_del'].value()]
        new_owner.extend([own.id for own in User.objects.filter(id__in=bound_form_2['owner_to_add'].value())])
        new_test = [test.id for test in theme.get_test() if
                        str(test.id) not in bound_form_2['test_to_del'].value()]
        new_test.extend([test.id for test in Test.objects.filter(id__in=bound_form_2['test_to_add'].value())])
        new_kata = [kata.id for kata in theme.get_kata() if
                    str(kata.id) not in bound_form_2['kata_to_del'].value()]
        new_kata.extend([kata.id for kata in Kata.objects.filter(id__in=bound_form_2['kata_to_add'].value())])

        if bound_form.is_valid():
            new_theme=bound_form.save()
            new_theme.owner.set(new_owner)
            new_theme.test.set(new_test)
            new_theme.kata.set(new_kata)
            new_theme.save()
            return redirect(new_theme)
        return render(request,'educa/theme_update.html',{'form':bound_form})
class ThemeDeleteView(LoginRequiredMixin,TypeCourseDeleteMixin,View):
    model = Theme
    url = 'themes_list_url'
    templates='educa/theme_delete.html'
class TestsListView(LoginRequiredMixin,TypeCourseListMixin,View):
    model=Test
    templates='educa/tests_list.html'


class TestDetailView(LoginRequiredMixin,TypeCourseDetailMixin,View):
    model = Test
    templates = 'educa/test_detail.html'
class TestCreateView(LoginRequiredMixin,View):

    def get(self,request):
        form=TestForm()
        return render(request,'educa/test_create.html',{'form':form})

    def post(self,request):
        bound_form=TestForm(request.POST)
        if bound_form.is_valid():
            new_test=bound_form.save()
            return redirect(new_test)
        return render(request,'educa/test_create.html',{'form':bound_form})
class TestUpdateView(LoginRequiredMixin,View):

    def get(self,request,pk):
        test=Test.objects.get(id=pk)
        form=ThemeForm(instance=test)
        form_2=OwnerUpdateForm()
        context = {'form': form,
                   'test':test,
                   'owner_to_del': form_2['owner_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in test.get_owner()])),
                   'owner_to_add': form_2['owner_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in User.objects.all() if
                                own not in test.get_owner()])),
                   }
        return render(request,'educa/test_update.html',context=context)

    def post(self,request,pk):
        test = Test.objects.get(id=pk)
        bound_form = TestForm(request.POST,instance=test)
        bound_form_2=OwnerUpdateForm(request.POST)
        context = {'form': bound_form,
                   'test':test,
                   'owner_to_del': bound_form_2['owner_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in test.get_owner()])),
                   'owner_to_add': bound_form_2['owner_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in User.objects.all() if
                                own not in test.get_owner()])),
                   }
        new_owner = [own.id for own in test.get_owner() if
                         str(own.id) not in bound_form_2['owner_to_del'].value()]
        new_owner.extend([own.id for own in User.objects.filter(id__in=bound_form_2['owner_to_add'].value())])
        if bound_form.is_valid():
            new_test=bound_form.save()
            new_test.owner.set(new_owner)
            new_test.save()
            return redirect(new_test)
        return render(request,'educa/test_update.html',{'form':bound_form})
class TestDeleteView(LoginRequiredMixin,TypeCourseDeleteMixin,View):
    model = Test
    url = 'tests_list_url'
    templates='educa/test_delete.html'

class TestBaseTextView(LoginRequiredMixin,View):
    def get(self,request,pk):
        dict_text={}
        test=Test.objects.get(id=pk)
        file='tests'+str(test.base)
        with open('media/'+str(test.base)) as f:
            text = json.load(f)
        for key,value in text.items():
            dict_text[key]=value
        return render(request,'educa/test_base_text.html',{'dict_text':dict_text})

class KatasListView(LoginRequiredMixin,TypeCourseListMixin,View):
    model=Kata
    templates='educa/katas_list.html'


class KataDetailView(LoginRequiredMixin,TypeCourseDetailMixin,View):
    model = Kata
    templates = 'educa/kata_detail.html'

class KataCreateView(LoginRequiredMixin,View):

    def get(self,request):
        form=KataForm()
        return render(request,'educa/kata_create.html',{'form':form})

    def post(self,request):
        bound_form=KataForm(request.POST)
        if bound_form.is_valid():
            new_kata=bound_form.save()
            return redirect(new_kata)
        return render(request,'educa/kata_create.html',{'form':bound_form})
class KataUpdateView(LoginRequiredMixin,View):

    def get(self,request,pk):
        kata=Kata.objects.get(id=pk)
        form=KataForm(instance=kata)
        form_2=OwnerUpdateForm()
        context = {'form': form,
                   'kata':kata,
                   'owner_to_del': form_2['owner_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in kata.get_owner()])),
                   'owner_to_add': form_2['owner_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in User.objects.all() if
                                own not in kata.get_owner()])),
                   }
        return render(request,'educa/kata_update.html',context=context)

    def post(self,request,pk):
        kata = Test.objects.get(id=pk)
        bound_form = KataForm(request.POST,instance=kata)
        bound_form_2=OwnerUpdateForm(request.POST)
        context = {'form': bound_form,
                   'kata':kata,
                   'owner_to_del': bound_form_2['owner_to_del'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in kata.get_owner()])),
                   'owner_to_add': bound_form_2['owner_to_add'].as_widget(forms.CheckboxSelectMultiple(
                       choices=[(own.id, own.username) for own in User.objects.all() if
                                own not in kata.get_owner()])),
                   }
        new_owner = [own.id for own in kata.get_owner() if
                         str(own.id) not in bound_form_2['owner_to_del'].value()]
        new_owner.extend([own.id for own in User.objects.filter(id__in=bound_form_2['owner_to_add'].value())])
        if bound_form.is_valid():
            new_kata=bound_form.save()
            new_kata.owner.set(new_owner)
            new_kata.save()
            return redirect(new_kata)
        return render(request,'educa/kata_update.html',{'form':bound_form})
class KataDeleteView(LoginRequiredMixin,TypeCourseDeleteMixin,View):
    model = Kata
    url = 'katas_list_url'
    templates='educa/kata_delete.html'

class InternEnrollInternShipView(LoginRequiredMixin,View):

    def post(self,request):
        form=CourseAddForm()
        internship=InternShip.objects.get(id=request.POST['internships'])
        internship.interns.add(request.user)
        internship.save()
        if not request.user.profile.assesments:
            request.user.profile.assesments = {}
        cache.set('internship', internship, 600)
        if str(internship.id) not in request.user.profile.assesments.keys():
            request.user.profile.assesments[internship.id] = {}

        request.user.profile.save()
        return render(request,'educa/intern_internships_list.html',{'internship':internship,
                            'form':form['courses'].as_widget(forms.CheckboxSelectMultiple(choices=[(cur.id,cur.name)
                                    for cur in internship.get_courses()]))})

class InternEnrollCourseView(LoginRequiredMixin,View):
    def post(self,request):
        form_dict={}
        form=ThemeAddForm()
        for course in Course.objects.filter(id__in=request.POST.getlist('courses')):
            key,value=course,form['themes'].as_widget(forms.CheckboxSelectMultiple(choices=[(th.id,th.name)
                                    for th in course.get_themes()]))
            form_dict[key]=value
            course.interns.add(request.user)
            course.save()
        cache.set('course', Course.objects.filter(id__in=request.POST.getlist('courses')), 600)
        for course in Course.objects.filter(id__in=request.POST.getlist('courses')):
            if cache.get('internship') is None:
                return redirect(reverse('internships_list_url'))
            request.user.profile.assesments[str(cache.get('internship').id)][course.id]= {}
            for theme in course.get_themes():
                theme.interns.add(request.user)
                theme.save()
                if not request.user.profile.assesments[str(cache.get('internship').id)][course.id]:
                    request.user.profile.assesments[str(cache.get('internship').id)][course.id]={}
                request.user.profile.assesments[str(cache.get('internship').id)][course.id][theme.id]={'kata':{},'test':{}}
                for kata in theme.get_kata():
                    request.user.profile.assesments[str(cache.get('internship').id)][course.id][theme.id]['kata'][kata.id] = 0
                for test in theme.get_test():
                    request.user.profile.assesments[str(cache.get('internship').id)][course.id][theme.id]['test'][test.id] = 0
                print(request.user.profile.assesments[str(cache.get('internship').id)][course.id][theme.id])
            request.user.profile.save()
        cache.clear()
        return render(request,'educa/intern_themes_list.html',{'courses':Course.objects.filter(id__in=request.POST.getlist('courses'))})

        #return render(request,'educa/intern_courses_list.html',{'course':course,'form':form_dict})

# class InternEnrollThemeView(LoginRequiredMixin,View):
#
#     def post(self,request):
#         print(dir(request.POST))
#         print(request.POST.lists())
#         #print(request.POST.fromkeys())
#         print(request.POST.__getattribute__)
#         print(request.POST.__getitem__)
#         cache.set('theme', Theme.objects.filter(id__in=request.POST.getlist('themes')), 600)
#         print(cache.get('theme'))
#         for theme in Theme.objects.filter(id__in=request.POST.getlist('themes')):
#             #theme=Theme.objects.get(id=request.POST['themes'])
#             theme.interns.add(request.user)
#             theme.save()
#         for course in  cache.get('course'):
#             print(course)
#             for theme in course.get_themes():
#                 print('1',theme)
#                 if theme in cache.get('theme'):
#                     print('2',theme)
#
#         return render(request,'educa/intern_themes_list.html',{'themes':Theme.objects.filter(id__in=request.POST.getlist('themes'))})

class StudentInternShipDetailView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'educa/student_internship_detail.html',
                    {'assesments':request.user.profile.assesments,'student':request.user})

class KataTrainView(LoginRequiredMixin,TrainMixin,View):
    model=Kata
    form=KataAnswerForm
    templates='educa/kata_train.html'
    templates_l='student_internship_detail_url'


class TestTrainView(LoginRequiredMixin,TrainMixin,View):
    model=Test
    form=TestAnswerForm
    templates='educa/test_train.html'
    templates_l='student_internship_detail_url'

class UnEnrollChoiceInternShipView(LoginRequiredMixin,View):

    def get(self,request):
        form_dict={}
        for internship_id in request.user.profile.assesments.keys():
            internship=InternShip.objects.get(id=int(internship_id))
            if len(Course.objects.filter(id__in=[int(cur) for cur in request.user.profile.assesments[internship_id]])) >0:
                key,value=InternShipEnrollForm(initial={'internships':internship.id}),Course.objects.filter(id__in=[int(cur) for cur in request.user.profile.assesments[internship_id]])
                form_dict[key]=value
        return render(request,'educa/intern_choice_unenroll_internship.html',{'form':form_dict})

class UnEnrollCourseChoiceView(LoginRequiredMixin,View):
    def post(self,request):
        internship = InternShip.objects.get(id=request.POST['internships'])
        cache.set('internship_un', internship, 600)
        form=UnEnrollCourseForm()
        query=Course.objects.filter(id__in=[int(cur) for cur in request.user.profile.assesments[str(internship.id)]])
        return render(request,'educa/intern_unenroll_course_list.html',{'internship':internship,'form':form['courses'].as_widget(forms.CheckboxSelectMultiple(choices=[(cur.id,cur.name)
                                for cur in query]))})

class UnEnrollCourseView(LoginRequiredMixin,View):
    def post(self,request):
        print(request.user.profile.assesments)

        if cache.get('internship_un') is None:
            return redirect(reverse('choice_internship_unenroll_url'))
        internship = InternShip.objects.get(id=cache.get('internship_un').id)
        for course in Course.objects.filter(id__in=request.POST.getlist('courses')):
            #request.user.profile.assesments.pop(str(cache.get('internship_un').id))
            request.user.profile.assesments[str(cache.get('internship_un').id)].pop(str(course.id))
            i=internship.get_courses()
            i.remove(course)
            internship.courses.set(i)
        request.user.profile.save()
        print(request.user.profile.assesments)
        return render(request,'educa/student_internship_detail.html',
                    {'assesments':request.user.profile.assesments,'student':request.user})

class ProjectEnrollView(LoginRequiredMixin,View):

    def post(self,request):
        project=Project.objects.get(id=request.POST['projects'])
        project.internshipers.add(request.user)
        project.save()
        report_name=request.user.username.replace(' ','_')+'_'+project.name.replace(' ','_')
        if not Report.objects.filter(name=report_name,internshiper=request.user,project=project).exists():
            report = Report.objects.create(name=report_name, internshiper=request.user, project=project,description={})
        return redirect(project)

class InternshiperDetailView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'educa/internshiper_project_detail.html',
                    {'assesments':request.user.profile.assesments,'internshiper':request.user})

class ReportsListView(LoginRequiredMixin,TypeCourseListMixin,View):
    model=Report
    templates='educa/reports_list.html'

class ReportDetailView(LoginRequiredMixin,TypeCourseDetailMixin,View):
    model = Report
    templates = 'educa/report_detail.html'

class ReportUpdateView(LoginRequiredMixin,View):
    def get(self,request,pk):
        report=Report.objects.get(id=pk)
        form=ReportUpdateForm(instance=report,initial={'edit_field':''})
        return render(request,'educa/report_update.html',{'report':report,'form':form})
    def post(self,request,pk):
        report=Report.objects.get(id=pk)
        bound_form=ReportUpdateForm(request.POST,instance=report,initial={'edit_field':''})
        if bound_form.is_valid():
                report.description[datetime.now().__str__()]=bound_form['edit_field'].value()
                report.save()
                return redirect(report)
        return render(request,'educa/report_update.html',{'report':report,'form':bound_form})

