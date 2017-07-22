from django.db import models
import datetime

# Create your models here.
class Grade(models.Model):
    course = models.CharField(max_length=128)
    university = models.CharField(max_length=16)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    credits = models.DecimalField(max_digits=3, decimal_places=1)
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Course: {} | Credits: {} | GPA: {}'.format(self.course, self.credits, self.gpa)

    def get_dict_form(self):
        grade_info = {}
        grade_info["course"] = self.course
        grade_info["gpa"] = self.gpa
        grade_info["credits"] = self.credits
        return grade_info

class CGPA(models.Model):
    cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    ip = models.GenericIPAddressField()
    university = models.CharField(max_length=16)
    def __str__(self):
        return "{} | {}".format(self.cgpa, self.ip)

class MultGrade(models.Model):
    course = models.CharField(max_length=256)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    credits = models.DecimalField(max_digits=3, decimal_places=1)
    ip = models.GenericIPAddressField()
    university = models.CharField(max_length=16)
    def __str__(self):
        return 'Course: {} | Credits: {} | GPA: {}'.format(self.course, self.credits, self.gpa)

    def get_dict_form(self):
        grade_info = {}
        grade_info["course"] = self.course
        grade_info["gpa"] = self.gpa
        grade_info["credits"] = self.credits
        return grade_info
