from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^login$',views.login),
    url(r'^process$',views.process),
    url(r'^login/process$',views.login_process),
    url(r'^success$',views.success),
    url(r'^logout$',views.logout),
    url(r'^job_index$',views.job_index),
    url(r'^create_job$',views.create_job),
    url(r'^create_job/process',views.create_job_process),
    url(r'^add_to_jobs/(\d+)$',views.add_to_jobs),
    url(r'^view/(\d+)$',views.view),
    url(r'^edit_job/(\d+)$',views.edit_job),
    url(r'^(\d+)$',views.edit_job_process),
    url(r'^delete/(\d+)$',views.delete),
    url(r'^give_up/(\d+)$',views.give_up),
    url(r'^answer/(\d+)$',views.answer_page),
    url(r'^answer/process/(\d+)$',views.answer_process),
    url(r'^answers$',views.answers_page),
    url(r'^master$',views.master)
]