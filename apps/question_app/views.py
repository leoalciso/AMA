from django.shortcuts import render, redirect 
from django.contrib import messages
from .models import User, Job, Answer
import bcrypt

def index(request):
    return render(request,'index.html')

def process(request):
    print('in validator')
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(index)
    print('valid arguments')
    print('hashing password')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    print('user hash:')
    print(pw_hash)
    User.objects.create(first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        email=request.POST['email'],
                        password=pw_hash)
    print('created user')
    return redirect(login)

def login(request):
    return render(request,'login.html')

def login_process(request):
    # print(request)
    if request.POST['email']=='teacher':
        return redirect('/master')
    if User.objects.filter(email=request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user.id'] = user.id
            return redirect(success)
    messages.error(request, 'email/password does not match')
    return redirect(login)
    
def master(request):
    context = {
        'students':User.objects.all()
    }
    return render(request,'master.html',context)
    
def success(request):
    if not request.session['user.id']:
        messages.error(request, 'you are not logged in :(')
        return redirect(login)
    print('in success')
    print(request.session['user.id'])
    this_user = User.objects.get(id=request.session['user.id'])
    context = {
        'this_user':this_user
    }
    return render(request,'success_page.html',context)

def logout(request):
    request.session['user.id'] = ''
    return redirect(index)
    
def job_index(request):
    this_user=User.objects.get(id=request.session['user.id'])
    context = {
        'this_user':User.objects.get(id=request.session['user.id']),
        'all_users':User.objects.all(),
        'all_jobs':Job.objects.all(),
        'user_matched_jobs':get_matches(this_user)
    }
    return render(request,'job_index.html',context)

def create_job(request):
    this_user = User.objects.get(id=request.session['user.id'])
    this_user.posts += 1;
    this_user.save()
    context = {
        'this_user':User.objects.get(id=request.session['user.id'])
    }
    return render(request,'create_job.html',context)

def create_job_process(request):
    print('in validator')
    print(request.POST)
    errors = Job.objects.validator(request.POST)
    this_user = User.objects.get(id=request.session['user.id'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(create_job)
    Job.objects.create(title=request.POST['title'],
                       description=request.POST['description'],
                    #    answer=Answer.objects.create(answer='',user_id=''),
                       category=request.POST['category'],
                       posted_by=this_user)
    return redirect(job_index)

def get_matches(this_user):
    new={}
    for index in Job.objects.all():
        this_job = Job.objects.get(id=index.id)
        try:
            if this_job.users_who_took.get(id=this_user.id):
                new[this_job]='true'  
        except:            
            new[this_job]='false'
    return new

def add_to_jobs(request,methods='GET'):
    print('adding to favorites')
    print(methods)
    this_user=User.objects.get(id=request.session['user.id'])
    this_job=Job.objects.get(id=methods)
    this_job.users_who_took.add(this_user)
    return redirect(job_index)

def view(request,methods='GET'):
    print('in view')
    print(methods)
    context = {
        'this_job':Job.objects.get(id=methods)
    }
    return render(request,'view_job.html',context)

def edit_job(request,methods='GET'):
    print(request.POST)
    print(methods)
    context = {
        'this_job':Job.objects.get(id=methods)
    }
    return render(request,'edit_job.html',context)
    
def edit_job_process(request,methods='GET'):
    print('in validator')
    print(request.POST)
    errors = Job.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'edit_job/{methods}')
    print('in process update')
    this_job=Job.objects.get(id=methods)
    this_job.title=request.POST['title']
    this_job.description=request.POST['description']
    this_job.category=request.POST['category']
    this_job.save()
    return redirect(job_index)

def delete(request,methods='GET'):
    this_job=Job.objects.get(id=methods)
    this_job.delete()
    return redirect(job_index)

def give_up(request,methods='GET'):
    this_user=request.session['user.id']
    this_job=Job.objects.get(id=methods)
    this_job.users_who_took.remove(this_user)
    return redirect(job_index)

def answer_page(request,methods='GET'):
    context = {
        'this_job':Job.objects.get(id=methods),
        'answer':Answer.objects.all()
    }
    return render(request,'answer.html',context)

def answer_process(request,methods='GET'):
    this_user = User.objects.get(id=request.session['user.id'])
    this_user.answers += 1;
    this_user.save()
    Answer.objects.create(answer=request.POST['answer'],
                          user_id=request.session['user.id'])
    print(request.POST['answer'])
    print(methods)
    return redirect(f'/answer/{methods}')

def get_matches_finished(this_user):
    new={}
    for index in Job.objects.all():
        this_job = Job.objects.all()
        try:
            if this_job.posted_by.get(id=this_user.id):
                new[this_job]='true'
        except:
            new[this_job]='false'
    return new

def answers_page(request):
    this_user=request.session['user.id']
    context={
        'answers':get_matches_finished(this_user)
    }
    print(context['answers'])
    return render(request,'answered.html',context)