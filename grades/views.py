from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Grade, CGPA, MultGrade
import json

# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def list(request, *args, **kwargs):
    path = request.path.strip('/')
    print("path: ", path)
    print("request: ", request)
    if path == "uoft":
        UNIV = 'uoft'
    elif path == "york":
        UNIV = 'york'
    else:
        UNIV = 'ryerson'
    user_ip = get_client_ip(request)
    if (request.method == "POST"):
        qd = request.POST
        UNIV = qd["uni"] # prevents user changes in url continuing to databases
        Grade.objects.filter(ip=user_ip, university=UNIV).delete()
        CGPA.objects.filter(ip=user_ip, university=UNIV).delete()
        CGPA.objects.create(cgpa=qd["cgpa"], ip=user_ip, university=UNIV)
        MultGrade.objects.filter(ip=user_ip, university=UNIV).delete()
        MultGrade.objects.create(gpa=qd["previous-GPA"], course=qd["previous-course"], credits=qd['previous-credits'], ip=user_ip, university=UNIV)
        for i in range(1, len(qd)//3 - 1):
            #qd contains 3 items per course row + a django token
            # course numberings start from 1
            course_key = "course_" + str(i)
            gpa_key = "gpa_" + str(i)
            credits_key = "credits_" + str(i)
            print(type(qd[gpa_key]))
            print(qd[gpa_key])
            if qd[gpa_key] != "None": # if grade is none, i.e. an unused row is ignored
                obj = Grade.objects.create(course=qd[course_key], gpa=qd[gpa_key], credits=qd[credits_key],university=UNIV, ip=user_ip)
                obj.save()
    qs = Grade.objects.filter(ip=user_ip, university=UNIV)
    qs2 = CGPA.objects.filter(ip=user_ip, university=UNIV)
    qs3 = MultGrade.objects.filter(ip=user_ip, university=UNIV)
    context={"rows": len(qs), "courses":[]}

    if qs2:
        context["cgpa"] = qs2[0].cgpa
    if qs3:
        context["mult"] = qs3[0]
    else:
        qs3 = MultGrade.objects.create(ip=user_ip, gpa=0, credits=0.0, course="", university=UNIV )
        context['mult']=qs3
    print(context)
    unique_count = 0
    for course in qs:
        unique_count += 1
        dict_ = course.get_dict_form()
        dict_["count"] = unique_count
        context['courses'].append(dict_)
    context['UNIV'] = UNIV
    return render(request,'index.html',context)

def about(request, *args, **kwargs):
    context = {}
    return render(request,'about.html',context)
