from typing import Any
from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.views import LoginView

def weby(request):
    return render(request,'base/weby.html')

class CustomLoginView(LoginView):
    template_name='base/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('TaskList')
    
class RegisterView(FormView):
    template_name='base/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('TaskList')

    def form_valid(self, form: Any):
        user=form.save()
        if user:
            login(self.request,user)
        return super(RegisterView,self).form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('TaskList')
        return super(RegisterView,self).get(*args,**kwargs)

class TaskList(LoginRequiredMixin,ListView):
    model=Task 
    context_object_name='tasks'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context= super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(status=False).count()

        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(
                title__icontains=search_input)
            context['count']=context['tasks'].filter(status=False).count()
        context['search_input']=search_input  
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='task'
    template_name='base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description','status']
    success_url=reverse_lazy('TaskList')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','status']
    success_url=reverse_lazy('TaskList')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    success_url=reverse_lazy('TaskList')


