from django import template
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


register=template.Library()

@register.filter(name='has_group')
def has_group(user,group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()

@register.filter
def by_kata(dictionary, internship_position):
    return dictionary[str(internship_position)]

@register.simple_tag
def kata_assesment(dictionary, internship_position,course_position,theme_position,type,type_position):
    try:
        return dictionary[str(internship_position)][str(course_position)][str(theme_position)][type][str(type_position)]
    except:
        pass

@register.simple_tag
def theme_assesment(dictionary, internship_position,course_position,theme_position):
    summ=0.0
    for key, value in dictionary[str(internship_position)][str(course_position)][str(theme_position)].items():
        summ+=sum([v for v in value.values()])
    return summ

@register.simple_tag
def course_assesment(dictionary, internship_position,course_position):
    summ=0.0
    for key, value in dictionary[str(internship_position)][str(course_position)].items():
        summ+=sum([sum(v1) for v1 in [v.values() for v in value.values()]])
    return summ

@register.simple_tag
def internship_assesment(dictionary, internship_position):
    summ=0.0
    for key, value in dictionary[str(internship_position)].items():
        for k,v in value.items():
            summ+=sum([sum(v2) for v2 in [v1.values() for v1 in v.values()]])
    return summ
