from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models

class UserManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData['first_name']) < 2:
            errors['first_name']='first name must have 2 characters minimum'
        if len(postData['last_name']) < 2:
            errors['last_name']='last name must have 2 characters minimum'
        try:
            validate_email(postData['email']) 
        except ValidationError as e:
            errors['email']='invalid email'
        if len(postData['password']) < 8:
            errors['password']='password must be 8 characters minimum'
        if postData['password']!=postData['confirm_password']:
            errors['match']='passwords do not match'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    posts = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)
    objects = UserManager()

    def __repr__ (self):
        return str(self.__dict__)
    
class Answer(models.Model):
    answer = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    
    def __repr__ (self):
        return str(self.__dict__)    
    
class JobManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData['title']) < 3:
            errors['title']='title must have 3 characters minimum'
        if len(postData['description']) < 3:
            errors['description']='description must have 3 characters minimum'
        if len(postData['category']) < 3:
            errors['category']='category must have 3 characters minimum'
        return errors
    
class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name='jobs_uploaded')
    users_who_took = models.ManyToManyField(User, related_name='liked_jobs')
    answer = models.ForeignKey(Answer, related_name='answer_to_q',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()
    
    def __repr__ (self):
        return str(self.__dict__)
