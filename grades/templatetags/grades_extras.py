from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def user_friendly_label(value):
    value = float(value)
    if (value == 5.0):
        return "A+: 90-100"
    if (value == 4.0):
        return "A : 85-89"
    if (value == 3.7):
        return "A-: 80-84"
    if (value == 3.3):
        return "B+: 77-79"
    if (value == 3.0):
        return "B : 73-76"
    if (value == 2.7):
        return "B-: 70-72"
    if (value == 2.3):
        return "C+: 67-69"
    if (value == 2.0):
        return "C : 63-66"
    if (value == 1.7):
        return "C-: 60-62"
    if (value == 1.3):
        return "D+: 57-59"
    if (value == 1.0):
        return "D : 53-56"
    if (value == 0.7):
        return "D-: 50-52"
    if (value == 0.0):
        return "F : 0-49"
    return "None"
