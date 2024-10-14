from django.shortcuts import render, redirect,reverse
import json

class TypeCourseListMixin:
    model=None
    templates=None

    def get(self,request):
        if self.model.__name__=='Report':
            objs=self.model.objects.filter(internshiper=request.user)
        else:
            objs=self.model.objects.all()
        return render(request,self.templates,{self.model.__name__.lower()+'s':objs})

class TypeCourseDetailMixin:
    model=None
    templates=None
    form=None

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        if self.form:
            enroll_form=self.form(initial={self.model.__name__.lower()+'s':obj.id})
            return render(request, self.templates, {self.model.__name__.lower(): obj,'enroll_form':enroll_form})
        return render(request, self.templates, {self.model.__name__.lower(): obj})

class TypeCourseDeleteMixin:
    model = None
    templates = None
    url=None
    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        print(obj)
        return render(request, self.templates, {self.model.__name__.lower(): obj})

    def post(self, request, pk):
        obj = self.model.objects.get(id=pk)
        print(obj)
        obj.delete()
        print('DEL')
        return redirect(reverse(self.url))

class TrainMixin:
    model=None
    form=None
    templates=None
    templates_l=None
    form_model=None

    def get(self,request,internship_id,course_id,theme_id,pk):
        obj=self.model.objects.get(id=pk)
        form=self.form()
        if self.model.__name__=='Test':
            dict_text = {}
            file = 'tests' + str(obj.base)
            with open('media/' + str(obj.base)) as f:
                text = json.load(f)
            for key, value in text.items():
                dict_text[key] = ' '
            form=self.form(initial={'answer':dict_text})
        context={
            self.model.__name__.lower(): obj,
            'form': form,
            'internship_id': internship_id,
            'course_id':course_id,
            'theme_id':theme_id,
        }
        return render(request,self.templates,context=context)

    def post(self,request,internship_id,course_id,theme_id,pk):
        obj = self.model.objects.get(id=pk)
        bound_form = self.form(request.POST)
        context = {
            self.model.__name__.lower(): obj,
            'form': bound_form,
            'internship_id': internship_id,
            'course_id': course_id,
            'theme_id': theme_id,
        }
        if bound_form.is_valid():
            if self.model.__name__ == 'Test':
                if  obj.compare_answer(bound_form['answer'].value())>0:
                    request.user.profile.assesments[str(internship_id)][str(course_id)][str(theme_id)][
                        self.model.__name__.lower()][str(pk)] =obj.compare_answer(bound_form['answer'].value())
                    request.user.profile.save()
                    return redirect(reverse(self.templates_l))
                else:
                    message = "Ответ неправильный"
                    context['message'] = message
                    return render(request, self.templates, context=context)

            if bound_form['answer'].value().lower()==obj.solution.lower():
                request.user.profile.assesments[str(internship_id)][str(course_id)][str(theme_id)][self.model.__name__.lower()][str(pk)]=5
                request.user.profile.save()
                return redirect(reverse(self.templates_l))
            else:
                message="Ответ неправильный"
                context['message']=message
                return render(request,self.templates,context=context)
        else:

            return render(request, self.templates, context=context)
# class TypeCourseUpdateMixin:
#     model = None
#     templates = None
#     form=None
#     form_=None
#
#     def get(self,request,pk):
#         theme=Theme.objects.get(id=pk)
#         form=ThemeForm(instance=theme)
#         form_2=ThemeUpdateForm()
#         print(dir(ThemeUpdateForm))
#         print(ThemeUpdateForm.base_fields)
#         print(dir(ThemeUpdateForm.base_fields))
#         context = {'form': form,
#                    'theme':theme,
#                    'owner_to_del': form_2['owner_to_del'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(own.id, own.username) for own in theme.get_owner()])),
#                    'owner_to_add': form_2['owner_to_add'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(own.id, own.username) for own in User.objects.all() if
#                                 own not in theme.get_owner()])),
#                    'test_to_del': form_2['test_to_del'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(test.id, test.name) for test in theme.get_test()])),
#                    'teste_to_add': form_2['test_to_add'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(test.id, test.name) for test in Test.objects.all() if
#                                 test not in theme.get_test()])),
#                    'kata_to_del': form_2['kata_to_del'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(kata.id, kata.name) for kata in theme.get_kata()])),
#                    'kata_to_add': form_2['kata_to_add'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(kata.id, kata.name) for kata in Kata.objects.all() if
#                                 kata not in theme.get_kata()])),
#                    }
#         return render(request,'educa/theme_update.html',context=context)
#
#     def post(self,request,pk):
#         theme = Theme.objects.get(id=pk)
#         bound_form = ThemeForm(request.POST,instance=theme)
#         bound_form_2=ThemeUpdateForm(request.POST)
#         context = {'form': bound_form,
#                    'theme': theme,
#                    'owner_to_del': bound_form_2['owner_to_del'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(own.id, own.username) for own in theme.get_owner()])),
#                    'owner_to_add': bound_form_2['owner_to_add'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(own.id, own.username) for own in User.objects.all() if
#                                 own not in theme.get_owner()])),
#                    'test_to_del': bound_form_2['test_to_del'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(test.id, test.name) for test in theme.get_test()])),
#                    'teste_to_add': bound_form_2['test_to_add'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(test.id, test.name) for test in Test.objects.all() if
#                                 test not in theme.get_test()])),
#                    'kata_to_del': bound_form_2['kata_to_del'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(kata.id, kata.name) for kata in theme.get_kata()])),
#                    'kata_to_add': bound_form_2['kata_to_add'].as_widget(forms.CheckboxSelectMultiple(
#                        choices=[(kata.id, kata.name) for kata in Kata.objects.all() if
#                                 kata not in theme.get_kata()])),
#                    }
#         new_owner = [own.id for own in theme.get_owner() if
#                          str(own.id) not in bound_form_2['owner_to_del'].value()]
#         new_owner.extend([own.id for own in User.objects.filter(id__in=bound_form_2['owner_to_add'].value())])
#         new_test = [test.id for test in theme.get_test() if
#                         str(test.id) not in bound_form_2['test_to_del'].value()]
#         new_test.extend([test.id for test in Test.objects.filter(id__in=bound_form_2['test_to_add'].value())])
#         new_kata = [kata.id for kata in theme.get_kata() if
#                     str(kata.id) not in bound_form_2['kata_to_del'].value()]
#         new_kata.extend([kata.id for kata in Kata.objects.filter(id__in=bound_form_2['kata_to_add'].value())])
#
#         if bound_form.is_valid():
#             new_theme=bound_form.save()
#             new_theme.owner.set(new_owner)
#             new_theme.test.set(new_test)
#             new_theme.kata.set(new_kata)
#             new_theme.save()
#             return redirect(new_theme)
#         return render(request,'educa/theme_update.html',{'form':bound_form})
