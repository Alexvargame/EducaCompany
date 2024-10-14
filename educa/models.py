from django.db import models
from django.shortcuts import reverse

from django.contrib.auth.models import User

import json
class Direction(models.Model):

    name=models.CharField(max_length=100)
    class Meta:
        verbose_name='Направление'
        verbose_name_plural='Направления'

    def __str__(self):
        return self.name



class Project(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    direction=models.ManyToManyField(Direction,related_name='project_directions')
    director=models.ManyToManyField(User,related_name='project_directors')
    task=models.CharField(max_length=1000)
    internshipers=models.ManyToManyField(User,related_name='internshiper_joined',blank=True)
    #report=models.ForeignKey(User,related_name='reports',on_delete=models.DO_NOTHING,default=1)


    class Meta:
        verbose_name='Проект'
        verbose_name_plural='Проекты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail_url',kwargs={'pk':self.id})
    def get_delete_url(self):
        return reverse('project_delete_url',kwargs={'pk':self.id})
    def get_direction(self):
        return [dirs for dirs in self.direction.all()]

    def get_director(self):
        return [direct for direct in self.director.all()]

class InternShip(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    direction = models.ManyToManyField(Direction, related_name='intern_directions')
    director = models.ManyToManyField(User, related_name='intern_directors')
    interns=models.ManyToManyField(User,related_name='internship_joined',blank=True)

    class Meta:
        verbose_name='Интернатура'
        verbose_name_plural='Интернатуры'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('internship_detail_url', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('internship_delete_url',kwargs={'pk':self.id})

    def get_update_url(self):
        return reverse('internship_update_url',kwargs={'pk':self.id})

    def get_direction(self):
        return [dirs for dirs in self.direction.all()]

    def get_interns(self):
        return[intern for intern in self.interns.all()]

    def get_director(self):
        return [direct for direct in self.director.all()]

    def get_courses(self):
        return [intern for intern in self.courses.all()]

class Course(models.Model):
    name=models.CharField(max_length=250,blank=True,null=True)
    owner=models.ManyToManyField(User, related_name='course_owners')
    internship=models.ManyToManyField(InternShip,related_name='courses',blank=True)
    type = models.CharField(choices=[('theory', 'theory'), ('practic', 'practic')], max_length=50)
    interns=models.ManyToManyField(User,related_name='course_joined',blank=True)




    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name

    def get_internship(self):
        return [i for i in self.internship.all()]

    def get_owner(self):
        return [own for own in self.owner.all()]
    def get_interns(self):
        return[intern for intern in self.interns.all()]

    def get_themes(self):
        return [theme for theme in self.course_themes.all()]

    def get_absolute_url(self):
        return reverse('course_detail_url', kwargs={'pk': self.id})
    def get_delete_url(self):
        return reverse('course_delete_url',kwargs={'pk':self.id})
    def get_update_url(self):
        return reverse('course_update_url',kwargs={'pk':self.id})

class Kata(models.Model):
    name=models.CharField(max_length=250)
    owner=models.ManyToManyField(User, related_name='kata_owners')
    base=models.CharField(max_length=1000,blank=True)
    solution = models.CharField(default='', max_length=100)


    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kata_detail_url', kwargs={'pk': self.id})

    def get_owner(self):
        return [own for own in self.owner.all()]
    def get_themes(self):
        return [th for th in self.kata_themes.all()]
    def get_delete_url(self):
        return reverse('kata_delete_url',kwargs={'pk':self.id})
    def get_update_url(self):
        return reverse('kata_update_url',kwargs={'pk':self.id})
    # def kata_train(self):
    #     return reverse('kata_train_url',args=[internship.id,course.id,theme.id,self.id})



def get_test_file_path(instance):
    return 'test/'+str(instance.base)
    #return os.path.join('tests/'+f'{instance.memorytest.place_name}',filename)
class Test(models.Model):
    name = models.CharField(max_length=250)
    owner=models.ManyToManyField(User, related_name='test_owners')
    base = models.FileField(default='default.json',upload_to='tests/')
    solution=models.CharField(default='',max_length=100)
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('test_detail_url', kwargs={'pk': self.id})

    def get_owner(self):
        return [own for own in self.owner.all()]
    def get_themes(self):
        return [th for th in self.test_themes.all()]

    def get_delete_url(self):
        return reverse('test_delete_url',kwargs={'pk':self.id})
    def get_update_url(self):
        return reverse('test_update_url',kwargs={'pk':self.id})

    def compare_answer(self,other):
        count=0
        ans=json.loads(other)
        sol=json.loads(self.solution)
        for key in ans.keys():
            if sol[key]==ans[key]:
                count+=1
        if count>len(ans)/3*2-1:
            return count
        return 0
class Theme(models.Model):

    name=models.CharField(max_length=250)
    owner = models.ManyToManyField(User, related_name='theme_owners')
    course=models.ManyToManyField(Course,related_name='course_themes',blank=True)
    kata=models.ManyToManyField(Kata,related_name='kata_themes',blank=True)
    test=models.ManyToManyField(Test,related_name='test_themes',blank=True)
    interns=models.ManyToManyField(User,related_name='theme_joined',blank=True)



    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('theme_detail_url', kwargs={'pk': self.id})


    def get_kata(self):
        return [k for k in self.kata.all()]

    def get_test(self):
        return [t for t in self.test.all()]
    def get_course(self):
        return [c for c in self.course.all()]

    def get_owner(self):
        return [own for own in self.owner.all()]
    def get_interns(self):
        return[intern for intern in self.interns.all()]

    def get_delete_url(self):
        return reverse('theme_delete_url',kwargs={'pk':self.id})
    def get_update_url(self):
        return reverse('theme_update_url',kwargs={'pk':self.id})

class Report(models.Model):

    name=models.CharField(max_length=100, blank=True,null=True)
    description=models.JSONField(blank=True,null=True)
    edit_field=models.TextField(blank=True,null=True)
    internshiper=models.ForeignKey(User,related_name='internshiper_report',on_delete=models.DO_NOTHING)
    project=models.ForeignKey(Project,related_name='project_report',on_delete=models.DO_NOTHING)
    date_created=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Отчет'
        verbose_name_plural='Отчеты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('report_detail_url', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('report_update_url', kwargs={'pk': self.id})


