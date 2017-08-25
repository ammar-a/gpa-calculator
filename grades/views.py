from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Grade, CGPA, MultGrade
import json, string, random
# Create your views here.
def get_client_id_(request):
    if 'user_id' in request.COOKIES:
        return request.COOKIES['user_id']
def generate_id(size=5, chars=string.ascii_lowercase + string.digits + string.ascii_uppercase):
    user_id = ''.join(random.choice(chars) for _ in range(size))
    already_exists = CGPA.objects.filter(user_id=user_id).exists()
    if already_exists:
        return generate_id()
    return user_id
def list(request, *args, **kwargs):
    path = request.path.strip('/')
    print("path: ", path)
    print("request: ", request)
    if path == "uoft":
        UNIV = "uoft"
    elif path == "york":
        UNIV = "york"
    else:
        UNIV = "ryerson"
    user_id = get_client_id_(request)
    if not user_id:
        user_id = generate_id()
    if (request.method == "POST"):
        qd = request.POST #query dictionary
        UNIV = qd["uni"] # prevents user changes in url continuing to databases
        CGPA.objects.filter(user_id=user_id, university=UNIV).delete()
        CGPA.objects.create(cgpa=qd["cgpa"], user_id=user_id, university=UNIV)
        MultGrade.objects.filter(user_id=user_id, university=UNIV).delete()
        MultGrade.objects.create(gpa=qd["previous-GPA"], course=qd["previous-course"], credits=qd['previous-credits'], user_id=user_id, university=UNIV)
        Grade.objects.filter(user_id=user_id, university=UNIV).delete()
        for i in range(1, len(qd)//3 - 1):
            #qd contains 3 items per course row + a django token
            # course numberings start from 1
            course_key = "course_" + str(i)
            gpa_key = "gpa_" + str(i)
            credits_key = "credits_" + str(i)
            print(type(qd[gpa_key]))
            print(qd[gpa_key])
            if qd[gpa_key] != "None": # if grade is none, i.e. an unused row is ignored
                obj = Grade.objects.create(course=qd[course_key], gpa=qd[gpa_key], credits=qd[credits_key],university=UNIV, user_id=user_id)
                obj.save()
    qs = Grade.objects.filter(user_id=user_id, university=UNIV)
    qs2 = CGPA.objects.filter(user_id=user_id, university=UNIV)
    qs3 = MultGrade.objects.filter(user_id=user_id, university=UNIV)
    context={"rows": len(qs), "courses":[]}

    if qs2:
        context["cgpa"] = qs2[0].cgpa
    if qs3:
        context["mult"] = qs3[0]
    else:
        qs3 = MultGrade.objects.create(user_id=user_id, gpa=0, credits=0.0, course="", university=UNIV )
        context['mult']=qs3
    print(context)
    unique_count = 0
    for course in qs:
        unique_count += 1
        dict_ = course.get_dict_form()
        dict_["count"] = unique_count
        context['courses'].append(dict_)
    context['UNIV'] = UNIV
    context['active'] = UNIV
    response = render(request,'index.html',context)
    response.set_cookie('user_id', user_id)
    return response

def about(request, *args, **kwargs):
    context = {"active": "about"}
    return render(request,'about.html',context)
